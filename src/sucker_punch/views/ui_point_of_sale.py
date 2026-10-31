# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'point_of_sale.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_PointOfSale(object):
    def setupUi(self, PointOfSale):
        if not PointOfSale.objectName():
            PointOfSale.setObjectName('PointOfSale')
        PointOfSale.resize(1200, 700)
        PointOfSale.setStyleSheet(
            'QWidget#centralwidget { background: white; }\n'
            'QTableView { background: white; color: black; gridline-color: #dcdcdc; border: 1px solid #b0b0b0; }\n'
            'QTableView::item { padding: 0 4px; }\n'
            'QTableView::item:selected { background: #e6ff8c; color: black; }\n'
            'QTableView QLineEdit { background: #ffff80; color: black; border: none;\n'
            '                      selection-background-color: #1d4ed8; selection-color: white; }\n'
            'QHeaderView::section { background: #f4f6fb; color: #000080; font-weight: bold;\n'
            '                       border: none; border-bottom: 2px solid #000080; padding: 6px 4px; }\n'
            'QLabel#lbl_help { color: #707070; }\n'
            'QLabel#lbl_not_found { color: #b00020; }\n'
            'QLabel#lbl_date_title, QLabel#lbl_total_title { color: #000080; font-weight: bold; }\n'
            'QFrame#frameTotals { background: #fafafa; border: 1px solid #c8c8c8; border-radius: 4px; }\n'
            'QFrame#frameTotals QLabel { background: transparent; }\n'
            'QLabel#lbl_t0_value, QLabel#lbl_tiva_value, QLabel#lbl_iva_value, QLabel#lbl_discount_value'
            ', QLabel#lbl_ice_value {\n'
            '    background: #e3f5e3; border: 1px solid #9ccc9c; padding: 2px 8px; }\n'
            'QLabel#lbl_total { background: #e3f5e3; border: 1px solid #9ccc9c; border-radius: 4px;\n'
            '                   color: black; font-weight: bold; padding: 2px 14px; }\n'
            'QPushButton#push_save { background: #f4f6fb; color: #000080; border: 1px solid #000080;\n'
            '                        border-radius: 4px; padding: 6px 14px; font-weight: bold; }\n'
            'QPushButton#push_save:hover { background: #e6ff8c; }'
        )
        self.centralwidget = QWidget(PointOfSale)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName('verticalLayout')
        self.frameHeader = QFrame(self.centralwidget)
        self.frameHeader.setObjectName('frameHeader')
        self.frameHeader.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frameHeader)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.txt_find = QLineEdit(self.frameHeader)
        self.txt_find.setObjectName('txt_find')
        self.txt_find.setMaximumSize(QSize(520, 16777215))
        self.txt_find.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.txt_find)

        self.lbl_not_found = QLabel(self.frameHeader)
        self.lbl_not_found.setObjectName('lbl_not_found')

        self.horizontalLayout.addWidget(self.lbl_not_found)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lbl_date_title = QLabel(self.frameHeader)
        self.lbl_date_title.setObjectName('lbl_date_title')

        self.horizontalLayout.addWidget(self.lbl_date_title)

        self.lbl_date = QLabel(self.frameHeader)
        self.lbl_date.setObjectName('lbl_date')

        self.horizontalLayout.addWidget(self.lbl_date)

        self.verticalLayout.addWidget(self.frameHeader)

        self.table_lines = QTableWidget(self.centralwidget)
        if self.table_lines.columnCount() < 10:
            self.table_lines.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter)
        self.table_lines.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter)
        self.table_lines.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignTrailing | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignTrailing | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignTrailing | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignTrailing | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter)
        self.table_lines.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignTrailing | Qt.AlignVCenter)
        self.table_lines.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.table_lines.setObjectName('table_lines')
        self.table_lines.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table_lines.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.table_lines.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_lines.setAlternatingRowColors(False)
        self.table_lines.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_lines.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_lines.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.table_lines.horizontalHeader().setMinimumSectionSize(30)
        self.table_lines.horizontalHeader().setHighlightSections(False)
        self.table_lines.horizontalHeader().setStretchLastSection(False)
        self.table_lines.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table_lines)

        self.lbl_help = QLabel(self.centralwidget)
        self.lbl_help.setObjectName('lbl_help')
        self.lbl_help.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_help)

        self.frameTotals = QFrame(self.centralwidget)
        self.frameTotals.setObjectName('frameTotals')
        self.frameTotals.setFrameShape(QFrame.Shape.StyledPanel)
        self.horizontalLayout_2 = QHBoxLayout(self.frameTotals)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.lbl_t0 = QLabel(self.frameTotals)
        self.lbl_t0.setObjectName('lbl_t0')

        self.horizontalLayout_2.addWidget(self.lbl_t0)

        self.lbl_t0_value = QLabel(self.frameTotals)
        self.lbl_t0_value.setObjectName('lbl_t0_value')
        self.lbl_t0_value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_t0_value)

        self.lbl_tiva = QLabel(self.frameTotals)
        self.lbl_tiva.setObjectName('lbl_tiva')

        self.horizontalLayout_2.addWidget(self.lbl_tiva)

        self.lbl_tiva_value = QLabel(self.frameTotals)
        self.lbl_tiva_value.setObjectName('lbl_tiva_value')
        self.lbl_tiva_value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_tiva_value)

        self.lbl_iva = QLabel(self.frameTotals)
        self.lbl_iva.setObjectName('lbl_iva')

        self.horizontalLayout_2.addWidget(self.lbl_iva)

        self.lbl_iva_value = QLabel(self.frameTotals)
        self.lbl_iva_value.setObjectName('lbl_iva_value')
        self.lbl_iva_value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_iva_value)

        self.lbl_discount = QLabel(self.frameTotals)
        self.lbl_discount.setObjectName('lbl_discount')

        self.horizontalLayout_2.addWidget(self.lbl_discount)

        self.lbl_discount_value = QLabel(self.frameTotals)
        self.lbl_discount_value.setObjectName('lbl_discount_value')
        self.lbl_discount_value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_discount_value)

        self.lbl_ice = QLabel(self.frameTotals)
        self.lbl_ice.setObjectName('lbl_ice')

        self.horizontalLayout_2.addWidget(self.lbl_ice)

        self.lbl_ice_value = QLabel(self.frameTotals)
        self.lbl_ice_value.setObjectName('lbl_ice_value')
        self.lbl_ice_value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_ice_value)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.push_save = QPushButton(self.frameTotals)
        self.push_save.setObjectName('push_save')
        self.push_save.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_2.addWidget(self.push_save)

        self.lbl_total_title = QLabel(self.frameTotals)
        self.lbl_total_title.setObjectName('lbl_total_title')

        self.horizontalLayout_2.addWidget(self.lbl_total_title)

        self.lbl_total = QLabel(self.frameTotals)
        self.lbl_total.setObjectName('lbl_total')
        self.lbl_total.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_2.addWidget(self.lbl_total)

        self.verticalLayout.addWidget(self.frameTotals)

        PointOfSale.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(PointOfSale)
        self.statusbar.setObjectName('statusbar')
        PointOfSale.setStatusBar(self.statusbar)

        self.retranslateUi(PointOfSale)

        QMetaObject.connectSlotsByName(PointOfSale)

    # setupUi

    def retranslateUi(self, PointOfSale):
        PointOfSale.setWindowTitle(
            QCoreApplication.translate('PointOfSale', 'Punto de Venta', None)
        )
        self.txt_find.setPlaceholderText(
            QCoreApplication.translate(
                'PointOfSale',
                'Buscar en la factura (Ctrl+F): c\u00f3digo o descripci\u00f3n, Enter = siguiente',
                None,
            )
        )
        self.lbl_not_found.setText('')
        self.lbl_date_title.setText(
            QCoreApplication.translate('PointOfSale', 'Fecha', None)
        )
        self.lbl_date.setText(
            QCoreApplication.translate('PointOfSale', '01-01-2026 00:00', None)
        )
        ___qtablewidgetitem = self.table_lines.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate('PointOfSale', 'Nro.', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'number', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem1 = self.table_lines.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate('PointOfSale', 'C\u00f3digo de Barras', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem1.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'code', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem2 = self.table_lines.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate('PointOfSale', 'UM', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem2.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'uom', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem3 = self.table_lines.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate('PointOfSale', 'Descripci\u00f3n', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem3.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'name', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem4 = self.table_lines.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate('PointOfSale', 'Cantidad', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem4.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'quantity', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem5 = self.table_lines.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate('PointOfSale', 'Precio Unit.', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem5.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'price', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem6 = self.table_lines.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate('PointOfSale', '% Desc', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem6.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'discount', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem7 = self.table_lines.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate('PointOfSale', 'TOTAL', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem7.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'subtotal', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem8 = self.table_lines.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate('PointOfSale', 'IVA', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem8.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'tax', None)
        )
        # endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem9 = self.table_lines.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(
            QCoreApplication.translate('PointOfSale', 'ICE', None)
        )
        # if QT_CONFIG(whatsthis)
        ___qtablewidgetitem9.setWhatsThis(
            QCoreApplication.translate('PointOfSale', 'ice', None)
        )
        # endif // QT_CONFIG(whatsthis)
        self.lbl_help.setText(
            QCoreApplication.translate(
                'PointOfSale',
                'Enter: buscar    F9: inventario    \u2191 \u2193: cambiar de l\u00ednea    5.CODIGO: cantidad 5    F2: cambiar precio    Shift+F6: borrar l\u00ednea    Ctrl+F: buscar en la factura    Ctrl+L: limpiar    Ctrl+P: reimprimir    Ctrl+Enter: guardar',
                None,
            )
        )
        self.lbl_t0.setText(QCoreApplication.translate('PointOfSale', 'Tarifa 0%', None))
        self.lbl_t0_value.setText(QCoreApplication.translate('PointOfSale', '0.00', None))
        self.lbl_tiva.setText(
            QCoreApplication.translate('PointOfSale', 'Tarifa IVA', None)
        )
        self.lbl_tiva_value.setText(
            QCoreApplication.translate('PointOfSale', '0.00', None)
        )
        self.lbl_iva.setText(QCoreApplication.translate('PointOfSale', 'IVA', None))
        self.lbl_iva_value.setText(
            QCoreApplication.translate('PointOfSale', '0.00', None)
        )
        self.lbl_discount.setText(
            QCoreApplication.translate('PointOfSale', 'Desc.', None)
        )
        self.lbl_discount_value.setText(
            QCoreApplication.translate('PointOfSale', '0.00', None)
        )
        self.lbl_ice.setText(QCoreApplication.translate('PointOfSale', 'ICE', None))
        self.lbl_ice_value.setText(
            QCoreApplication.translate('PointOfSale', '0.00', None)
        )
        self.push_save.setText(
            QCoreApplication.translate('PointOfSale', 'Guardar  (Ctrl+Enter)', None)
        )
        self.lbl_total_title.setText(
            QCoreApplication.translate('PointOfSale', 'TOTAL', None)
        )
        self.lbl_total.setText(QCoreApplication.translate('PointOfSale', '0.00', None))

    # retranslateUi
