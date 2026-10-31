# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ticket_preview.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_TicketPreview(object):
    def setupUi(self, TicketPreview):
        if not TicketPreview.objectName():
            TicketPreview.setObjectName(u"TicketPreview")
        TicketPreview.resize(560, 760)
        TicketPreview.setStyleSheet(u"QDialog { background: white; }\n"
"QScrollArea#scroll_paper { background: #e6e6e6; border: 1px solid #c8c8c8; }\n"
"QWidget#paper_area { background: #e6e6e6; }\n"
"QLabel#lbl_help { color: #707070; }")
        self.verticalLayout = QVBoxLayout(TicketPreview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scroll_paper = QScrollArea(TicketPreview)
        self.scroll_paper.setObjectName(u"scroll_paper")
        self.scroll_paper.setWidgetResizable(True)
        self.paper_area = QWidget()
        self.paper_area.setObjectName(u"paper_area")
        self.paper_area.setGeometry(QRect(0, 0, 538, 680))
        self.layout_paper = QHBoxLayout(self.paper_area)
        self.layout_paper.setObjectName(u"layout_paper")
        self.layout_paper.setContentsMargins(16, 16, 16, 16)
        self.scroll_paper.setWidget(self.paper_area)

        self.verticalLayout.addWidget(self.scroll_paper)

        self.lbl_help = QLabel(TicketPreview)
        self.lbl_help.setObjectName(u"lbl_help")
        self.lbl_help.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_help)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setObjectName(u"layout_buttons")
        self.spacer_buttons = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_buttons.addItem(self.spacer_buttons)

        self.push_close = QPushButton(TicketPreview)
        self.push_close.setObjectName(u"push_close")
        self.push_close.setAutoDefault(True)

        self.layout_buttons.addWidget(self.push_close)


        self.verticalLayout.addLayout(self.layout_buttons)


        self.retranslateUi(TicketPreview)

        self.push_close.setDefault(True)


        QMetaObject.connectSlotsByName(TicketPreview)
    # setupUi

    def retranslateUi(self, TicketPreview):
        TicketPreview.setWindowTitle(QCoreApplication.translate("TicketPreview", u"Simulaci\u00f3n de impresora", None))
        self.lbl_help.setText(QCoreApplication.translate("TicketPreview", u"As\u00ed saldr\u00eda impresa. No se mand\u00f3 a la impresora.", None))
        self.push_close.setText(QCoreApplication.translate("TicketPreview", u"Cerrar (Esc)", None))
    # retranslateUi

