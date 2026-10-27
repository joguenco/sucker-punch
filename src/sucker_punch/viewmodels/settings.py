from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog

from ..models.settings import Settings
from ..services.odoo_client import OdooClient, OdooError
from ..views.ui_settings import Ui_Settings


class SettingsDialog(QDialog):
    """Configuración: conexión a Odoo, tamaño de letra y aviso de stock.

    Enter guarda, Esc cancela, Espacio marca o desmarca la casilla.

    Al lado de cada dato dice de dónde sale: Sistema, .env o Por defecto. Lo que viene de
    una variable de entorno del sistema queda bloqueado, porque se cambia en Windows.
    """

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.settings = settings
        # campo → (editor, etiqueta de origen)
        self.fields = {
            'url': (self.ui.txt_url, self.ui.lbl_url_source),
            'database': (self.ui.txt_database, self.ui.lbl_database_source),
            'api_key': (self.ui.txt_api_key, self.ui.lbl_api_key_source),
            'font_size': (self.ui.spin_font_size, self.ui.lbl_font_size_source),
            'stock_warning': (
                self.ui.chk_stock_warning,
                self.ui.lbl_stock_warning_source,
            ),
        }

        self.ui.txt_url.setText(settings.url)
        self.ui.txt_database.setText(settings.database)
        self.ui.txt_api_key.setText(settings.api_key)
        self.ui.spin_font_size.setValue(settings.font_size)
        self.ui.chk_stock_warning.setChecked(settings.stock_warning)
        self.update_preview(settings.font_size)
        for field, (editor, source) in self.fields.items():
            source.setText(settings.sources.get(field, ''))
            editor.setEnabled(not settings.is_from_system(field))

        self.ui.spin_font_size.valueChanged.connect(self.update_preview)
        self.ui.push_test.clicked.connect(self.test_connection)
        self.ui.push_save.clicked.connect(self.save)
        self.ui.push_cancel.clicked.connect(self.reject)
        editable = [editor for editor, _ in self.fields.values() if editor.isEnabled()]
        (editable[0] if editable else self.ui.push_save).setFocus()

    def form_settings(self) -> Settings:
        return Settings(
            url=self.ui.txt_url.text().strip(),
            database=self.ui.txt_database.text().strip(),
            api_key=self.ui.txt_api_key.text().strip(),
            font_size=self.ui.spin_font_size.value(),
            stock_warning=self.ui.chk_stock_warning.isChecked(),
            sources=self.settings.sources,
        )

    def update_preview(self, size: int):
        font = QFont(self.ui.lbl_preview.font())
        font.setPointSize(size)
        self.ui.lbl_preview.setFont(font)

    def test_connection(self):
        settings = self.form_settings()
        if not settings.is_complete:
            self.ui.lbl_status.setText(
                '❌ Llena la dirección, la base de datos y la clave API.'
            )
            return
        odoo = OdooClient(settings)
        try:
            version = odoo.version()
            uid = odoo.call('res.users', 'context_get').get('uid')
            name = odoo.call('res.users', 'read', ids=[uid], fields=['login'])[0]['login']
        except OdooError as error:
            self.ui.lbl_status.setText(f'❌ {error}')
            return
        self.ui.lbl_status.setText(
            f'✔ Conectado a Odoo {version}, base {settings.database}. '
            f'La clave API es del usuario «{name}».'
        )

    def save(self):
        settings = self.form_settings()
        if not settings.is_complete:
            self.ui.lbl_status.setText(
                '❌ Llena la dirección, la base de datos y la clave API.'
            )
            return
        self.settings = settings
        self.accept()
