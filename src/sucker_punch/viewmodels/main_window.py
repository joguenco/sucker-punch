from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox

from sucker_punch.viewmodels.login import Login

from ..models.session import Session
from ..services.odoo_client import OdooClient, OdooError
from ..services.settings_service import SettingsService
from ..views.ui_main_window import Ui_MainWindow
from .point_of_sale import PointOfSale
from .settings import SettingsDialog
from .theme import apply_font_size


class MainWindow(QMainWindow):
    """Menú principal. Todo por teclado: flechas para elegir, Enter para entrar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()
        self.odoo: OdooClient | None = None
        self.session: Session | None = None
        self.point_of_sale: PointOfSale | None = None

        self.ui.push_poin_sale.clicked.connect(self.open_point_of_sale)
        self.ui.push_configuration.clicked.connect(self.open_settings)

        self.is_authenticated = self.try_login()
        if self.is_authenticated:
            self.ui.statusbar.showMessage(
                f'{self.session.user_name} · {self.session.company_name} · '
                f'{self.odoo.url} ({self.odoo.database})'
            )
            self.ui.push_poin_sale.setFocus()

    def owner(self):
        """Padre para los diálogos. Mientras el menú no se ve (antes del login) van sin
        padre: así tienen su propio botón en la barra de tareas."""
        return self if self.isVisible() else None

    def try_login(self) -> bool:
        while True:
            if not self.settings.is_complete:
                QMessageBox.information(
                    self.owner(),
                    'Configuración',
                    'Primero configura la conexión a Odoo: dirección, base de datos y '
                    'clave API. Al guardar se crea el archivo .env.',
                )
                if not self.open_settings():
                    return False
                continue
            login = Login(self.owner())
            if login.exec() != QDialog.DialogCode.Accepted:
                return False
            odoo = OdooClient(self.settings)
            try:
                self.session = odoo.login(login.user.name, login.user.password)
            except OdooError as error:
                message = QMessageBox(
                    QMessageBox.Icon.Warning, 'Ingreso', str(error), parent=self.owner()
                )
                message.addButton('Volver a intentar', QMessageBox.ButtonRole.AcceptRole)
                configure = message.addButton(
                    'Configuración', QMessageBox.ButtonRole.ActionRole
                )
                message.exec()
                if message.clickedButton() is configure:
                    self.open_settings()
                continue
            self.odoo = odoo
            return True

    def open_settings(self) -> bool:
        dialog = SettingsDialog(self.settings, self.owner())
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return False
        old = self.settings
        try:
            self.settings_service.save(dialog.settings)
            self.settings = self.settings_service.load()  # para ver de nuevo el origen
        except OSError as error:
            # Ej.: el .exe está en Program Files, donde solo escribe el administrador
            self.settings = dialog.settings
            folder = self.settings_service.path.parent
            QMessageBox.warning(
                self.owner(),
                'Configuración',
                f'No se pudo guardar el archivo .env en {folder} ({error.strerror}).\n'
                'Los datos se usan solo hasta cerrar la app.',
            )
        apply_font_size(self.settings.font_size)
        connection_changed = (old.url, old.database, old.api_key) != (
            self.settings.url,
            self.settings.database,
            self.settings.api_key,
        )
        if self.session and connection_changed:
            QMessageBox.information(
                self,
                'Configuración',
                'La nueva conexión a Odoo se usa la próxima vez que abras la app.',
            )
        return True

    def open_point_of_sale(self):
        # Sin padre: una ventana con padre no tiene botón en la barra de tareas, y con el
        # menú escondido la app solo se encontraba con Win+Tab
        self.point_of_sale = PointOfSale(
            self.odoo, self.session, stock_warning=self.settings.stock_warning
        )
        self.point_of_sale.closed.connect(self.show_menu)
        self.point_of_sale.show()
        self.hide()

    def show_menu(self):
        self.show()
        self.ui.push_poin_sale.setFocus()

    def keyPressEvent(self, event):
        # Flechas para moverse entre los botones (Enter los presiona)
        if event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Left):
            self.focusPreviousChild()
        elif event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Right):
            self.focusNextChild()
        else:
            super().keyPressEvent(event)
