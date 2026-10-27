"""Las líneas de la factura dentro de la tabla de point_of_sale.ui (un QTableWidget).

Las columnas se editan en Qt Designer: título, orden, alineación y letra. El código
reconoce cada columna por su nombre interno, escrito en la propiedad «whatsThis» del
encabezado: number, code, uom, name, quantity, price, discount, subtotal, tax, ice.

Siempre hay una fila en blanco al final para escribir o escanear el próximo código. Solo
se editan el código y, con F2, el precio.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from ..models.sale_line import SaleLine
from ..services.odoo_totals import money

# Ancho mínimo de cada columna y su peso: si sobra ancho, se reparte según el peso
WIDTHS = {
    'number': (50, 0),
    'code': (150, 2),
    'uom': (90, 0),
    'name': (220, 6),
    'quantity': (90, 1),
    'price': (110, 1),
    'discount': (70, 0),
    'subtotal': (100, 1),
    'tax': (50, 0),
    'ice': (70, 0),
}
DEFAULT_WIDTH = (80, 0)  # una columna nueva agregada en Designer
EDITABLE = ('code', 'price')


class SaleLinesTable:
    def __init__(self, table: QTableWidget):
        self.table = table
        self.lines: list[SaleLine] = []
        self.keys = [
            table.horizontalHeaderItem(column).whatsThis()
            for column in range(table.columnCount())
        ]
        table.setRowCount(1)
        self._fill(0)

    def column(self, key: str) -> int:
        return self.keys.index(key)

    @property
    def blank_row(self) -> int:
        return len(self.lines)

    @property
    def draft(self) -> str:
        """Lo escrito en la fila en blanco y todavía no buscado."""
        return self.table.item(self.blank_row, self.column('code')).text()

    @draft.setter
    def draft(self, text: str):
        # Cambiar UNA celda también actualiza el editor si está abierto
        self.table.item(self.blank_row, self.column('code')).setText(text)

    def add_line(self, line: SaleLine):
        row = self.blank_row
        self.lines.append(line)
        self.table.insertRow(row)  # la fila en blanco baja una posición
        self._fill(row)
        self._fill(row + 1)  # la fila en blanco queda vacía y con su nuevo número

    def replace_line(self, row: int, line: SaleLine):
        self.lines[row] = line
        self._fill(row)

    def remove_line(self, row: int):
        """Borra la fila: las de abajo suben y se renumeran."""
        del self.lines[row]
        self.table.removeRow(row)
        for below in range(row, self.table.rowCount()):
            self._set(below, 'number', str(below + 1))

    def clear_draft(self):
        self.draft = ''

    def clear(self):
        self.lines.clear()
        self.table.setRowCount(0)
        self.table.setRowCount(1)
        self._fill(0)

    def _values(self, row: int) -> dict[str, str]:
        if row == self.blank_row:
            return {'number': str(row + 1), 'code': ''}
        line = self.lines[row]
        product = line.product
        return {
            'number': str(row + 1),
            'code': product.code,
            'uom': product.uom,
            'name': product.name,
            'quantity': f'{line.quantity:.2f}',
            'price': f'{line.price:.4f}',
            'discount': '0.00',
            'subtotal': f'{money(line.subtotal):.2f}',
            'tax': f'{product.tax_percent:g}',
            'ice': '0.00',
        }

    def _fill(self, row: int):
        values = self._values(row)
        for key in self.keys:
            self._set(row, key, values.get(key, ''))

    def _set(self, row: int, key: str, text: str):
        if key not in self.keys:  # columna quitada en Designer
            return
        column = self.keys.index(key)
        item = self.table.item(row, column)
        if item is None:
            item = QTableWidgetItem()
            # Cada celda se alinea como el encabezado de su columna (se elige en Designer)
            alignment = self.table.horizontalHeaderItem(column).textAlignment()
            item.setTextAlignment(
                Qt.AlignmentFlag(alignment) | Qt.AlignmentFlag.AlignVCenter
            )
            flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
            if key in EDITABLE:
                flags |= Qt.ItemFlag.ItemIsEditable
            item.setFlags(flags)
            self.table.setItem(row, column, item)
        item.setText(text)
