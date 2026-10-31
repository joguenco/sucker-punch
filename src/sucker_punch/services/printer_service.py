"""Impresoras instaladas (Windows, o CUPS en Linux) y el dibujo de la factura.

El mismo dibujo sirve para el papel y para Simular impresora: letra de ancho fijo con
COLUMNS caracteres por línea, como la vista en pantalla de DonPos. Con impresoras de
Windows el corte del papel y el cajón los maneja el driver de la impresora.
"""

from PySide6.QtCore import QPointF
from PySide6.QtGui import QFont, QFontMetricsF, QPaintDevice, QPainter
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo

from ..models.ticket import PrintLine, Printout

COLUMNS = 42  # caracteres por línea (papel de 80 mm)
RECEIPT_WIDTH_MM = (
    72  # ancho máximo impreso: en una hoja A4 sale como tira a la izquierda
)
FONT_FAMILY = 'Courier New'


class PrinterError(Exception):
    """No se pudo imprimir."""


def printer_names() -> list[str]:
    return QPrinterInfo.availablePrinterNames()


def ticket_font() -> QFont:
    font = QFont(FONT_FAMILY)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFixedPitch(True)
    return font


class TicketDrawing:
    """Dibuja las líneas de la factura en un ancho dado (en pixeles del dispositivo)."""

    def __init__(self, device: QPaintDevice, width: float):
        self.font = ticket_font()
        # Tamaño de letra para que entren COLUMNS caracteres justo en el ancho
        self.font.setPixelSize(100)
        char_width = QFontMetricsF(self.font, device).horizontalAdvance('M')
        self.font.setPixelSize(max(1, int(100 * width / (COLUMNS * char_width))))
        metrics = QFontMetricsF(self.font, device)
        self.char_width = metrics.horizontalAdvance('M')
        self.line_height = metrics.lineSpacing()
        self.ascent = metrics.ascent()
        self.width = self.char_width * COLUMNS

    @staticmethod
    def scale(line: PrintLine) -> tuple[int, int]:
        """(ancho, alto) de la letra. size: 1 doble alto, 2 doble ancho, 3 los dos."""
        return (2 if line.size in (2, 3) else 1, 2 if line.size in (1, 3) else 1)

    def height(self, line: PrintLine) -> float:
        return self.line_height * self.scale(line)[1]

    def total_height(self, printout: Printout) -> float:
        return sum(self.height(line) for line in printout.lines)

    def draw_line(self, painter: QPainter, line: PrintLine, x: float, y: float):
        """Una línea con su tamaño, negritas y subrayado. El corte no se dibuja."""
        scale_x, scale_y = self.scale(line)
        painter.save()
        painter.translate(x, y)
        painter.scale(scale_x, scale_y)
        column = 0
        for part in line.texts:
            font = QFont(self.font)
            font.setBold(part.bold)
            font.setUnderline(part.underline)
            painter.setFont(font)
            painter.drawText(QPointF(column * self.char_width, self.ascent), part.text)
            column += len(part.text)
        painter.restore()


def print_printout(printout: Printout, printer_name: str):
    """Manda la factura a una impresora instalada."""
    info = QPrinterInfo.printerInfo(printer_name)
    if info.isNull():
        raise PrinterError(
            f'La impresora «{printer_name}» no está instalada en esta computadora. '
            'Elige otra en Configuración.'
        )
    printer = QPrinter(info, QPrinter.PrinterMode.HighResolution)
    printer.setDocName('Factura')
    paint_printout(printer, printout, printer_name)


def paint_printout(printer: QPrinter, printout: Printout, printer_name: str):
    """Dibuja la factura en el QPrinter, en una o más hojas."""
    painter = QPainter()
    if not painter.begin(printer):
        raise PrinterError(
            f'No se pudo imprimir en «{printer_name}». Revisa que esté encendida y '
            'conectada.'
        )
    try:
        page = printer.pageLayout().paintRectPixels(printer.resolution())
        max_width = RECEIPT_WIDTH_MM * printer.resolution() / 25.4
        drawing = TicketDrawing(printer, min(page.width(), max_width))
        y = 0.0
        for line in printout.lines:
            if line.cut:
                continue
            height = drawing.height(line)
            if y + height > page.height():  # hoja llena (impresoras de hojas)
                if not printer.newPage():
                    raise PrinterError(f'«{printer_name}» no aceptó otra hoja.')
                y = 0.0
            drawing.draw_line(painter, line, 0, y)
            y += height
    finally:
        painter.end()
