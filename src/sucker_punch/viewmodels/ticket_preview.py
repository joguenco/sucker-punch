from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPen
from PySide6.QtWidgets import QApplication, QDialog, QWidget

from ..models.ticket import Printout
from ..services.printer_service import (
    COLUMNS,
    TicketDrawing,
    print_printout,
    ticket_font,
)
from ..views.ui_ticket_preview import Ui_TicketPreview

MARGIN = 14  # pixeles de papel en blanco alrededor del texto
PAPER_FONT_SCALE = 0.8  # la factura con letra un poco más chica que la de la app
MIN_FONT_POINTS = 8  # más chica ya no se lee bien: ahí la factura se desplaza
MIN_WIDTH = 480  # ancho mínimo de la ventana, para los textos y el botón de abajo


def show_or_print(printout: Printout, printer: str, simulate: bool, parent=None):
    """Con Simular impresora la factura se muestra en pantalla; si no, se imprime."""
    if simulate:
        TicketPreview(printout, parent).exec()
    else:
        print_printout(printout, printer)


class TicketPaper(QWidget):
    """La tira de papel: la factura dibujada igual que en la impresora."""

    def __init__(self, printout: Printout, max_height: float = 0, parent=None):
        super().__init__(parent)
        self.printout = printout
        # Letra un poco más chica que la de la app (Configuración → Tamaño de letra), o
        # más todavía para que entre toda la factura en max_height, sin bajar de
        # MIN_FONT_POINTS
        points = round(QApplication.font().pointSize() * PAPER_FONT_SCALE)
        width = self.paper_width(max(points, MIN_FONT_POINTS))
        self.drawing = TicketDrawing(self, width)
        text_height = max_height - 2 * MARGIN
        if max_height and self.text_height() > text_height:
            width = max(
                self.paper_width(MIN_FONT_POINTS),
                width * text_height / self.text_height(),
            )
            self.drawing = TicketDrawing(self, width)
        self.setFixedSize(
            int(self.drawing.width) + 2 * MARGIN,
            int(self.text_height()) + 2 * MARGIN,
        )

    def paper_width(self, points: int) -> float:
        """Ancho de COLUMNS caracteres con letra de ese tamaño."""
        font = ticket_font()
        font.setPointSize(points)
        return COLUMNS * QFontMetricsF(font, self).horizontalAdvance('M')

    def text_height(self) -> float:
        return sum(
            self.drawing.line_height if line.cut else self.drawing.height(line)
            for line in self.printout.lines
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('white'))
        painter.setPen(QColor('#b0b0b0'))
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
        painter.setPen(QColor('black'))
        y = float(MARGIN)
        for line in self.printout.lines:
            if line.cut:
                self.draw_cut(painter, y)
                y += self.drawing.line_height
                continue
            self.drawing.draw_line(painter, line, MARGIN, y)
            y += self.drawing.height(line)
        painter.end()

    def draw_cut(self, painter: QPainter, y: float):
        """Donde la plantilla dice <cut/>: una línea punteada con la palabra corte."""
        middle = y + self.drawing.line_height / 2
        painter.save()
        painter.setPen(QPen(QColor('#909090'), 1, Qt.PenStyle.DashLine))
        painter.drawLine(QPointF(0, middle), QPointF(self.width(), middle))
        font = QFont(self.drawing.font)
        font.setItalic(True)
        painter.setFont(font)
        label = QRectF(0, y, self.width(), self.drawing.line_height)
        text = ' corte '
        text_width = QFontMetricsF(font, self).horizontalAdvance(text)
        painter.fillRect(
            QRectF((self.width() - text_width) / 2, y, text_width, label.height()),
            QColor('white'),
        )
        painter.drawText(label, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()


class TicketPreview(QDialog):
    """Simular impresora: la factura como saldría en el papel. Esc o Enter cierra."""

    def __init__(self, printout: Printout, parent=None):
        super().__init__(parent)
        self.ui = Ui_TicketPreview()
        self.ui.setupUi(self)
        # La ventana usa hasta el 90 % del alto de la pantalla. Lo que queda después de
        # los textos y el botón de abajo es para el papel: la factura se achica para
        # verse entera (si es muy larga, se desplaza)
        screen_height = int(self.screen().availableGeometry().height() * 0.9)
        rest = self.height_without_paper()
        paper = TicketPaper(printout, screen_height - rest, self.ui.paper_area)
        self.ui.layout_paper.addWidget(
            paper, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.ui.push_close.clicked.connect(self.accept)
        self.ui.push_close.setFocus()
        self.resize(
            max(paper.width() + 60, MIN_WIDTH),
            min(paper.height() + rest, screen_height),
        )

    def height_without_paper(self) -> int:
        """Alto de todo menos el papel: el texto de abajo (en el ancho de la ventana),
        el botón, los márgenes y el borde del área del papel."""
        self.ensurePolished()
        layout = self.layout()
        margins = layout.contentsMargins()
        width = MIN_WIDTH - margins.left() - margins.right()
        rows = [
            self.ui.lbl_help.heightForWidth(width),
            self.ui.push_close.sizeHint().height(),
        ]
        paper_margins = self.ui.layout_paper.contentsMargins()
        return (
            margins.top()
            + margins.bottom()
            + max(layout.spacing(), 0) * len(rows)
            + sum(rows)
            + 2 * self.ui.scroll_paper.frameWidth()
            + paper_margins.top()
            + paper_margins.bottom()
        )
