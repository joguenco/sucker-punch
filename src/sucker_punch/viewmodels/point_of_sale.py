"""Punto de Venta: la factura, todo por teclado.

Teclas en la celda del código:  Enter buscar · F9 inventario · F2 cambiar el precio ·
Shift+F6 borrar la línea (las de abajo suben) · ↑ ↓ cambiar de línea · "5.CODIGO" =
cantidad 5.
En toda la ventana:  Ctrl+Enter guardar (Pago Efectivo → Cambio) · Ctrl+F buscar una
línea en la factura · Ctrl+L limpiar la factura.
"""

import re
from collections import defaultdict
from datetime import datetime

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHeaderView,
    QMainWindow,
    QMessageBox,
)

from ..models.payment import Payment
from ..models.product import Product
from ..models.sale_line import SaleLine
from ..models.session import Session
from ..services.customer_service import CustomerService
from ..services.odoo_client import OdooClient, OdooError
from ..services.odoo_totals import compute_totals
from ..services.product_service import ProductService
from ..services.sale_service import SaleError, SaleService
from ..views.ui_point_of_sale import Ui_PointOfSale
from .barcode_delegate import BarcodeDelegate
from .change import ChangeDialog
from .payment import PaymentDialog
from .price_delegate import PriceDelegate
from .product_search import ProductSearch
from .sale_lines_table import DEFAULT_WIDTH, WIDTHS, SaleLinesTable
from .theme import busy

# "5.CODIGO" o "5*CODIGO" -> cantidad 5, busca "CODIGO". Decimales con coma o punto:
# "1,5.CODIGO", "1.5.CODIGO", "1.5*CODIGO"
QUANTITY_PREFIX = re.compile(r'^(\d+(?:[.,]\d+)?)[.*](.+)$')


def now_text() -> str:
    return datetime.now().astimezone().strftime('%d-%m-%Y %H:%M')


def split_quantity(text: str) -> tuple[float, str]:
    match = QUANTITY_PREFIX.match(text)
    if match:
        return float(match.group(1).replace(',', '.')), match.group(2).strip()
    return 1.0, text


class PointOfSale(QMainWindow):
    closed = Signal()  # el menú vuelve a aparecer

    def __init__(
        self,
        odoo: OdooClient,
        session: Session,
        parent=None,
        stock_warning: bool = True,  # Configuración → Avisar cuando no hay stock
    ):
        super().__init__(parent)
        self.ui = Ui_PointOfSale()
        self.ui.setupUi(self)
        self.session = session
        self.stock_warning = stock_warning
        self.products = ProductService(odoo)
        self.sales = SaleService(odoo, session.allowed_journal_ids)
        self.customers = CustomerService(odoo)
        self.row = 0  # fila del cursor (invoice.blank_row = fila en blanco del final)

        table = self.ui.table_lines
        self.invoice = SaleLinesTable(table)
        self.delegate = BarcodeDelegate(table)
        self.delegate.key_action.connect(self.on_key)
        table.setItemDelegateForColumn(self.invoice.column('code'), self.delegate)
        self.price_delegate = PriceDelegate(table)
        self.price_delegate.price_entered.connect(self.set_price)
        self.price_delegate.cancelled.connect(self.go_to)
        table.setItemDelegateForColumn(self.invoice.column('price'), self.price_delegate)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setSectionsClickable(False)
        table.clicked.connect(lambda index: self.go_to(index.row()))
        table.viewport().installEventFilter(self)  # clic en la parte vacía de la tabla

        self.ui.push_save.clicked.connect(self.save)
        for keys in (
            'Ctrl+Return',
            'Ctrl+Enter',
        ):  # Enter normal y el del teclado numérico
            QShortcut(QKeySequence(keys), self, self.save)
        QShortcut(QKeySequence('Ctrl+F'), self, self.focus_find)
        QShortcut(QKeySequence('Ctrl+L'), self, self.clear_invoice)
        self.ui.txt_find.returnPressed.connect(self.find_line)
        self.ui.txt_find.textChanged.connect(lambda: self.ui.lbl_not_found.clear())
        self.ui.txt_find.installEventFilter(self)

        self.ui.lbl_date.setText(now_text())
        self.ui.statusbar.showMessage(
            f'{session.user_name} · {session.company_name} · {odoo.url} ({odoo.database})'
        )
        self.update_totals()
        self.apply_font_sizes()

    # ---- Ventana ----
    def showEvent(self, event):
        super().showEvent(event)
        # Al abrir, el cursor ya queda en la celda 1 (código de la primera fila)
        QTimer.singleShot(0, lambda: self.go_to(self.row))

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.adjust_columns)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.FontChange:  # cambió el tamaño en Configuración
            self.apply_font_sizes()
        elif event.type() == QEvent.Type.ActivationChange and self.isActiveWindow():
            # Al salir de la app (Alt+Tab, clic en otro programa) Qt cierra el editor de
            # la celda: al volver se abre otra vez
            QTimer.singleShot(0, self.restore_cell)

    def apply_font_sizes(self):
        if getattr(self, '_applying_fonts', False):
            return
        self._applying_fonts = True
        # Los widgets con estilo (negritas, colores) no toman solos la letra nueva: volver
        # a poner el styleSheet los obliga a recalcularla
        self.setStyleSheet(self.styleSheet())
        self._applying_fonts = False
        size = self.font().pointSize()
        total_font = QFont(self.font())
        total_font.setPointSize(size * 2)
        total_font.setBold(True)
        self.ui.lbl_total.setFont(total_font)
        self.fit_totals()
        rows = self.ui.table_lines.verticalHeader()
        rows.setDefaultSectionSize(int(self.fontMetrics().height() * 1.8))
        self.adjust_columns()

    def adjust_columns(self):
        """Reparte el ancho de la tabla entre las columnas (se ve bien chica o grande)."""
        table = self.ui.table_lines
        scale = max(1.0, self.font().pointSize() / 12)
        sizes = [WIDTHS.get(key, DEFAULT_WIDTH) for key in self.invoice.keys]
        minimums = [int(minimum * scale) for minimum, _ in sizes]
        weights = [weight for _, weight in sizes]
        available = table.viewport().width()
        spare = max(0, available - sum(minimums))
        total_weight = sum(weights) or 1
        widths = [
            minimum + spare * weight // total_weight
            for minimum, weight in zip(minimums, weights)
        ]
        if spare:  # lo que sobra por redondeo, a la columna más ancha
            widths[weights.index(max(weights))] += available - sum(widths)
        elif sum(minimums) > available:  # letra grande en ventana chica: todo más angosto
            widths = [width * available // sum(minimums) for width in minimums]
        for column, width in enumerate(widths):
            table.setColumnWidth(column, width)

    # ---- Cursor ----
    def go_to(self, row: int, key: str = 'code'):
        """Pone el cursor en esa celda de la fila (el código), listo para escribir."""
        self.row = max(0, min(row, self.invoice.blank_row))
        table = self.ui.table_lines
        index = table.model().index(self.row, self.invoice.column(key))
        table.setCurrentIndex(index)
        table.setFocus()
        table.edit(index)
        table.scrollTo(index)  # solo mueve el scroll si la fila no se ve

    def restore_cell(self):
        """Si el foco quedó en la tabla sin celda abierta, abre la celda de la fila."""
        table = self.ui.table_lines
        editing = table.state() == QAbstractItemView.State.EditingState
        if self.focusWidget() is table and not editing:
            self.go_to(self.row)

    # ---- Teclas de la celda del código ----
    def on_key(self, action: str, text: str):
        if self.row == self.invoice.blank_row:
            self.invoice.draft = text
        if action == 'save':
            self.save()
        elif action == 'clear':
            self.clear_invoice()
        elif action == 'search':
            self.search(text.strip())
        elif action == 'inventory':
            quantity, term = split_quantity(text.strip())
            self.choose(quantity, term if '%' in term else f'{term}%')
        elif action == 'price':
            self.edit_price()
        elif action == 'delete':
            if self.row < self.invoice.blank_row:
                self.invoice.remove_line(self.row)  # las de abajo suben
                self.update_totals()
            else:
                self.invoice.clear_draft()
            self.go_to(self.row)
        elif action in ('up', 'down'):
            self.go_to(self.row + (-1 if action == 'up' else 1))

    def search(self, text: str):
        on_line = self.row < self.invoice.blank_row
        # Enter vacío, o con el mismo código de la línea: no se vuelve a buscar (si no,
        # la línea se rehacía y perdía su cantidad y el precio de F2); solo baja una fila
        if not text or (on_line and text == self.invoice.lines[self.row].product.code):
            self.go_to(self.row + 1 if on_line else self.row)
            return
        quantity, term = split_quantity(text)
        if quantity <= 0:
            QMessageBox.warning(self, 'Cantidad', 'La cantidad debe ser mayor que 0.')
            self.go_to(self.row)
            return
        try:
            exact = self.products.by_code(term)
            if len(exact) == 1:
                self.put_line(exact[0], quantity)
                return
            # No es un código exacto: buscar por "empieza con" y luego "contiene"
            pattern = f'{term}%'
            results = self.products.search(pattern)
            if not results:
                pattern = f'%{term}%'
                results = self.products.search(pattern)
        except OdooError as error:
            QMessageBox.critical(self, 'Error', str(error))
            self.go_to(self.row)
            return

        if not results:
            QMessageBox.warning(
                self, 'Artículo', f'No existe ningún artículo con «{term}».'
            )
            self.go_to(self.row)
        elif len(results) == 1:
            self.put_line(results[0], quantity)
        else:
            self.choose(quantity, pattern, results)

    def choose(self, quantity: float, pattern: str, results=None):
        dialog = ProductSearch(self.products, pattern, results, self)
        if dialog.exec() and dialog.selected:
            self.put_line(dialog.selected, quantity)
        else:
            self.go_to(self.row)

    def put_line(self, product: Product, quantity: float):
        if self.session.country_code == 'EC' and not product.tax_ids:
            # Sin impuesto de venta el XML de la factura sale inválido y el SRI no la
            # recibe («Element 'detalle': Missing child element(s)»)
            QMessageBox.warning(
                self,
                'Producto sin IVA',
                f'«{product.name}» no tiene impuesto de venta en Odoo y el SRI no '
                'acepta la factura.\n\nEn Odoo ponle IVA 0 % o IVA 15 % en '
                '«Impuestos de venta».',
            )
            self.go_to(self.row)
            return
        line = SaleLine(product=product, quantity=quantity)
        if self.row < self.invoice.blank_row:
            self.invoice.replace_line(self.row, line)
        else:
            self.invoice.add_line(line)
        self.update_totals()
        self.go_to(self.invoice.blank_row)  # salta a la fila en blanco del final

    # ---- Precio unitario (F2) ----
    def edit_price(self):
        if self.row >= self.invoice.blank_row:
            self.ui.statusbar.showMessage(
                'F2: primero ponte en una línea con producto.', 4000
            )
            self.go_to(self.row)
            return
        self.go_to(self.row, 'price')

    def set_price(self, row: int, price: float):
        """Precio nuevo solo para esta factura: se recalculan el total y el IVA."""
        line = self.invoice.lines[row]
        self.invoice.replace_line(row, line.model_copy(update={'price': price}))
        self.update_totals()
        self.go_to(row)

    # ---- Buscar una línea dentro de la factura (Ctrl+F) ----
    def focus_find(self):
        self.ui.txt_find.setFocus()
        self.ui.txt_find.selectAll()

    def find_line(self):
        text = self.ui.txt_find.text().strip().lower()
        if not text:
            self.go_to(self.row)
            return
        lines = self.invoice.lines
        for step in range(1, len(lines) + 1):
            row = (self.row + step) % (len(lines) + 1)  # empieza después del cursor
            if row < len(lines) and (
                text in lines[row].product.code.lower()
                or text in lines[row].product.name.lower()
            ):
                self.go_to(row)
                return
        self.ui.lbl_not_found.setText(f'«{text}» no está en la factura')

    def eventFilter(self, obj, event):
        # Esc en el buscador: volver a la tabla
        if (
            obj is self.ui.txt_find
            and event.type() == QEvent.Type.KeyPress
            and event.key() == Qt.Key.Key_Escape
        ):
            self.go_to(self.row)
            return True
        # Clic en la parte vacía de la tabla (debajo de las filas): la celda se cerraba
        table = self.ui.table_lines
        if (
            obj is table.viewport()
            and event.type() == QEvent.Type.MouseButtonRelease
            and not table.indexAt(event.position().toPoint()).isValid()
        ):
            QTimer.singleShot(0, self.restore_cell)
        return super().eventFilter(obj, event)

    # ---- Limpiar (Ctrl+L) ----
    def clear_invoice(self):
        """Deja la factura como recién abierta, sin cerrar la ventana."""
        count = len(self.invoice.lines)
        if count:
            answer = QMessageBox.question(
                self,
                'Limpiar',
                f'¿Limpiar la factura? Se quitan {count} línea(s).',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if answer != QMessageBox.StandardButton.Yes:
                self.go_to(self.row)
                return
        self.reset_invoice()

    def reset_invoice(self):
        self.invoice.clear()
        self.update_totals()
        self.ui.txt_find.clear()
        self.ui.lbl_date.setText(now_text())
        self.go_to(0)

    # ---- Totales y guardar ----
    def totals(self) -> dict:
        """Con el mismo redondeo que Odoo: el total y el vuelto salen iguales."""
        return compute_totals(self.invoice.lines, self.session.tax_rounding)

    def update_totals(self):
        totals = self.totals()
        self.ui.lbl_t0_value.setText(f'{totals["rate_0"]:.2f}')
        self.ui.lbl_tiva_value.setText(f'{totals["rate_vat"]:.2f}')
        self.ui.lbl_iva_value.setText(f'{totals["vat"]:.2f}')
        self.ui.lbl_total.setText(f'{totals["total"]:.2f}')
        self.fit_totals()

    def fit_totals(self):
        """Que cada total se vea completo con cualquier letra y ancho de ventana.

        El mínimo es el ancho de «0000.00» (así no saltan al cambiar el valor) o el del
        número actual si es más largo. Con un ancho fijo, una ventana angosta los
        aplastaba y se cortaba el primer dígito (14.00 se veía 4.00).
        """
        ui = self.ui
        for label in (
            ui.lbl_t0_value,
            ui.lbl_tiva_value,
            ui.lbl_iva_value,
            ui.lbl_discount_value,
            ui.lbl_ice_value,
            ui.lbl_total,
        ):
            metrics = label.fontMetrics()
            text = max(metrics.horizontalAdvance(t) for t in ('0000.00', label.text()))
            padding = label.width() - label.contentsRect().width()  # relleno y borde
            label.setMinimumWidth(text + padding)

    def check_stock(self, lines: list[SaleLine]) -> bool:
        """Avisa si se vende más de lo que hay en bodega (Odoo lo deja en negativo).

        Solo los productos con «Seguimiento de inventario»: los demás no llevan stock.
        """
        requested = defaultdict(float)
        for line in lines:
            requested[line.product.id] += line.quantity
        missing = {
            line.product.name: (requested[line.product.id], line.product.stock)
            for line in lines
            if line.product.is_storable
            and requested[line.product.id] > line.product.stock
        }
        if not missing:
            return True
        detail = '\n'.join(
            f'• {name}: pide {asked:g}, hay {stock:g}'
            for name, (asked, stock) in missing.items()
        )
        answer = QMessageBox.question(
            self,
            'Stock insuficiente',
            f'No alcanza el stock de:\n\n{detail}\n\n¿Guardar de todas formas?',
        )
        return answer == QMessageBox.StandardButton.Yes

    def save(self):
        """Ctrl+Enter: Pago Efectivo → Cambio (cliente) → se guarda en Odoo.

        Esc en Pago Efectivo vuelve a la factura; Esc en Cambio vuelve a Pago Efectivo.
        """
        lines = list(self.invoice.lines)
        if not lines:
            QMessageBox.information(self, 'Guardar', 'La factura no tiene productos.')
            self.go_to(self.row)
            return
        if self.stock_warning and not self.check_stock(lines):
            self.go_to(self.row)
            return

        total = self.totals()['total']
        payment = Payment(total=total, cash=total)
        customer = None
        while True:
            pay = PaymentDialog(payment, self)
            if pay.exec() != QDialog.DialogCode.Accepted:
                self.go_to(self.row)
                return
            payment = pay.payment
            change = ChangeDialog(
                payment,
                self.customers,
                limit_final_consumer=self.session.country_code == 'EC',
                customer=customer,
                parent=self,
            )
            accepted = change.exec() == QDialog.DialogCode.Accepted
            customer = change.customer or customer  # si vuelve, conserva el cliente
            if accepted:
                break

        try:
            with busy():
                result = self.sales.save(lines, customer.id, payment)
        except SaleError as error:
            QMessageBox.critical(self, 'No se guardó completa', str(error))
            self.go_to(self.row)
            return

        change_text = f'\nCambio: ${payment.change:.2f}' if payment.change else ''
        if abs(result.total - payment.total) >= 0.005:
            # No debería pasar (la pantalla calcula como Odoo), pero si pasa, que se vea
            # el vuelto correcto: el pago en efectivo ya se registró por lo que dijo Odoo
            right_change = max(0.0, payment.paid - result.total)
            change_text = (
                f'\n\n⚠ Odoo calculó ${result.total:.2f} y la pantalla '
                f'${payment.total:.2f}.\nVuelto correcto: ${right_change:.2f}'
            )
        customer_note = {
            'created': '  (✔ cliente nuevo)',
            'updated': '  (✔ cliente actualizado)',
        }.get(change.action, '')
        QMessageBox.information(
            self,
            'Compra realizada',
            f'✔ Compra realizada: factura {result.invoice}\n\n'
            f'Cliente: {customer.name}{customer_note}\n'
            f'Total: ${result.total:.2f}{change_text}\n'
            f'Estado: {result.payment_state}\nPedido: {result.order}',
        )
        self.reset_invoice()
