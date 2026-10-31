# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName('Settings')
        Settings.resize(680, 640)
        Settings.setStyleSheet(
            'QLabel#lbl_url_source, QLabel#lbl_database_source,\n'
            'QLabel#lbl_api_key_source, QLabel#lbl_font_size_source,\n'
            'QLabel#lbl_stock_warning_source, QLabel#lbl_printer_source,\n'
            'QLabel#lbl_printer_simulate_source {\n'
            '	color: #666666;\n'
            '}\n'
            '/* La casilla crece con el tama\u00f1o de letra (1em = alto de la letra) */\n'
            'QCheckBox::indicator { width: 1em; height: 1em; }'
        )
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName('verticalLayout')
        self.group_odoo = QGroupBox(Settings)
        self.group_odoo.setObjectName('group_odoo')
        self.gridLayout = QGridLayout(self.group_odoo)
        self.gridLayout.setObjectName('gridLayout')
        self.lbl_url = QLabel(self.group_odoo)
        self.lbl_url.setObjectName('lbl_url')

        self.gridLayout.addWidget(self.lbl_url, 0, 0, 1, 1)

        self.txt_url = QLineEdit(self.group_odoo)
        self.txt_url.setObjectName('txt_url')

        self.gridLayout.addWidget(self.txt_url, 0, 1, 1, 1)

        self.lbl_url_source = QLabel(self.group_odoo)
        self.lbl_url_source.setObjectName('lbl_url_source')
        self.lbl_url_source.setMinimumSize(QSize(90, 0))

        self.gridLayout.addWidget(self.lbl_url_source, 0, 2, 1, 1)

        self.lbl_database = QLabel(self.group_odoo)
        self.lbl_database.setObjectName('lbl_database')

        self.gridLayout.addWidget(self.lbl_database, 1, 0, 1, 1)

        self.txt_database = QLineEdit(self.group_odoo)
        self.txt_database.setObjectName('txt_database')

        self.gridLayout.addWidget(self.txt_database, 1, 1, 1, 1)

        self.lbl_database_source = QLabel(self.group_odoo)
        self.lbl_database_source.setObjectName('lbl_database_source')

        self.gridLayout.addWidget(self.lbl_database_source, 1, 2, 1, 1)

        self.lbl_api_key = QLabel(self.group_odoo)
        self.lbl_api_key.setObjectName('lbl_api_key')

        self.gridLayout.addWidget(self.lbl_api_key, 2, 0, 1, 1)

        self.txt_api_key = QLineEdit(self.group_odoo)
        self.txt_api_key.setObjectName('txt_api_key')
        self.txt_api_key.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.txt_api_key, 2, 1, 1, 1)

        self.lbl_api_key_source = QLabel(self.group_odoo)
        self.lbl_api_key_source.setObjectName('lbl_api_key_source')

        self.gridLayout.addWidget(self.lbl_api_key_source, 2, 2, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.group_odoo)

        self.group_display = QGroupBox(Settings)
        self.group_display.setObjectName('group_display')
        self.gridLayout_2 = QGridLayout(self.group_display)
        self.gridLayout_2.setObjectName('gridLayout_2')
        self.lbl_font_size = QLabel(self.group_display)
        self.lbl_font_size.setObjectName('lbl_font_size')

        self.gridLayout_2.addWidget(self.lbl_font_size, 0, 0, 1, 1)

        self.layout_font_size = QHBoxLayout()
        self.layout_font_size.setObjectName('layout_font_size')
        self.spin_font_size = QSpinBox(self.group_display)
        self.spin_font_size.setObjectName('spin_font_size')
        self.spin_font_size.setMinimum(10)
        self.spin_font_size.setMaximum(24)
        self.spin_font_size.setValue(14)

        self.layout_font_size.addWidget(self.spin_font_size)

        self.spacer_font_size = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.layout_font_size.addItem(self.spacer_font_size)

        self.gridLayout_2.addLayout(self.layout_font_size, 0, 1, 1, 1)

        self.lbl_font_size_source = QLabel(self.group_display)
        self.lbl_font_size_source.setObjectName('lbl_font_size_source')
        self.lbl_font_size_source.setMinimumSize(QSize(90, 0))

        self.gridLayout_2.addWidget(self.lbl_font_size_source, 0, 2, 1, 1)

        self.lbl_preview = QLabel(self.group_display)
        self.lbl_preview.setObjectName('lbl_preview')

        self.gridLayout_2.addWidget(self.lbl_preview, 1, 0, 1, 3)

        self.gridLayout_2.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.group_display)

        self.group_sales = QGroupBox(Settings)
        self.group_sales.setObjectName('group_sales')
        self.gridLayout_3 = QGridLayout(self.group_sales)
        self.gridLayout_3.setObjectName('gridLayout_3')
        self.chk_stock_warning = QCheckBox(self.group_sales)
        self.chk_stock_warning.setObjectName('chk_stock_warning')
        self.chk_stock_warning.setChecked(True)

        self.gridLayout_3.addWidget(self.chk_stock_warning, 0, 0, 1, 1)

        self.lbl_stock_warning_source = QLabel(self.group_sales)
        self.lbl_stock_warning_source.setObjectName('lbl_stock_warning_source')
        self.lbl_stock_warning_source.setMinimumSize(QSize(90, 0))

        self.gridLayout_3.addWidget(self.lbl_stock_warning_source, 0, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)

        self.verticalLayout.addWidget(self.group_sales)

        self.group_printer = QGroupBox(Settings)
        self.group_printer.setObjectName('group_printer')
        self.gridLayout_4 = QGridLayout(self.group_printer)
        self.gridLayout_4.setObjectName('gridLayout_4')
        self.lbl_printer = QLabel(self.group_printer)
        self.lbl_printer.setObjectName('lbl_printer')

        self.gridLayout_4.addWidget(self.lbl_printer, 0, 0, 1, 1)

        self.cmb_printer = QComboBox(self.group_printer)
        self.cmb_printer.setObjectName('cmb_printer')

        self.gridLayout_4.addWidget(self.cmb_printer, 0, 1, 1, 1)

        self.lbl_printer_source = QLabel(self.group_printer)
        self.lbl_printer_source.setObjectName('lbl_printer_source')
        self.lbl_printer_source.setMinimumSize(QSize(90, 0))

        self.gridLayout_4.addWidget(self.lbl_printer_source, 0, 2, 1, 1)

        self.chk_printer_simulate = QCheckBox(self.group_printer)
        self.chk_printer_simulate.setObjectName('chk_printer_simulate')

        self.gridLayout_4.addWidget(self.chk_printer_simulate, 1, 0, 1, 2)

        self.lbl_printer_simulate_source = QLabel(self.group_printer)
        self.lbl_printer_simulate_source.setObjectName('lbl_printer_simulate_source')
        self.lbl_printer_simulate_source.setMinimumSize(QSize(90, 0))

        self.gridLayout_4.addWidget(self.lbl_printer_simulate_source, 1, 2, 1, 1)

        self.push_test_printer = QPushButton(self.group_printer)
        self.push_test_printer.setObjectName('push_test_printer')
        self.push_test_printer.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.push_test_printer, 2, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.group_printer)

        self.lbl_status = QLabel(Settings)
        self.lbl_status.setObjectName('lbl_status')
        self.lbl_status.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_status)

        self.verticalSpacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frameButtons = QFrame(Settings)
        self.frameButtons.setObjectName('frameButtons')
        self.frameButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frameButtons)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.push_test = QPushButton(self.frameButtons)
        self.push_test.setObjectName('push_test')
        self.push_test.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.push_test)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.push_save = QPushButton(self.frameButtons)
        self.push_save.setObjectName('push_save')

        self.horizontalLayout.addWidget(self.push_save)

        self.push_cancel = QPushButton(self.frameButtons)
        self.push_cancel.setObjectName('push_cancel')
        self.push_cancel.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.push_cancel)

        self.verticalLayout.addWidget(self.frameButtons)

        # if QT_CONFIG(shortcut)
        self.lbl_printer.setBuddy(self.cmb_printer)
        # endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.txt_url, self.txt_database)
        QWidget.setTabOrder(self.txt_database, self.txt_api_key)
        QWidget.setTabOrder(self.txt_api_key, self.spin_font_size)
        QWidget.setTabOrder(self.spin_font_size, self.chk_stock_warning)
        QWidget.setTabOrder(self.chk_stock_warning, self.cmb_printer)
        QWidget.setTabOrder(self.cmb_printer, self.chk_printer_simulate)
        QWidget.setTabOrder(self.chk_printer_simulate, self.push_test_printer)
        QWidget.setTabOrder(self.push_test_printer, self.push_save)
        QWidget.setTabOrder(self.push_save, self.push_cancel)
        QWidget.setTabOrder(self.push_cancel, self.push_test)

        self.retranslateUi(Settings)

        self.push_save.setDefault(True)

        QMetaObject.connectSlotsByName(Settings)

    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(
            QCoreApplication.translate('Settings', 'Configuraci\u00f3n', None)
        )
        self.group_odoo.setTitle(
            QCoreApplication.translate('Settings', 'Conexi\u00f3n a Odoo', None)
        )
        self.lbl_url.setText(
            QCoreApplication.translate('Settings', 'Direcci\u00f3n', None)
        )
        self.txt_url.setPlaceholderText(
            QCoreApplication.translate('Settings', 'http://127.0.0.1:8019', None)
        )
        # if QT_CONFIG(tooltip)
        self.lbl_url_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_url_source.setText(QCoreApplication.translate('Settings', '.env', None))
        self.lbl_database.setText(
            QCoreApplication.translate('Settings', 'Base de datos', None)
        )
        self.txt_database.setPlaceholderText(
            QCoreApplication.translate('Settings', 'odoo19_ec', None)
        )
        # if QT_CONFIG(tooltip)
        self.lbl_database_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_database_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        self.lbl_api_key.setText(
            QCoreApplication.translate('Settings', 'Clave API', None)
        )
        self.txt_api_key.setPlaceholderText(
            QCoreApplication.translate(
                'Settings',
                'Odoo \u2192 Mis preferencias \u2192 Seguridad \u2192 Agregar clave API',
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.lbl_api_key_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_api_key_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        self.group_display.setTitle(
            QCoreApplication.translate('Settings', 'Pantalla', None)
        )
        self.lbl_font_size.setText(
            QCoreApplication.translate('Settings', 'Tama\u00f1o de letra', None)
        )
        self.spin_font_size.setSuffix(QCoreApplication.translate('Settings', ' pt', None))
        # if QT_CONFIG(tooltip)
        self.lbl_font_size_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_font_size_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        self.lbl_preview.setText(
            QCoreApplication.translate(
                'Settings',
                'As\u00ed se ver\u00e1 la letra: CHOCOLATE LISTO 220GR   $ 1.54',
                None,
            )
        )
        self.group_sales.setTitle(QCoreApplication.translate('Settings', 'Ventas', None))
        # if QT_CONFIG(tooltip)
        self.chk_stock_warning.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'Encendido: al guardar avisa si un producto no tiene stock suficiente. Apagado: no avisa y en Odoo el stock queda en negativo.',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.chk_stock_warning.setText(
            QCoreApplication.translate('Settings', 'Avisar cuando no hay stock', None)
        )
        # if QT_CONFIG(tooltip)
        self.lbl_stock_warning_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_stock_warning_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        self.group_printer.setTitle(
            QCoreApplication.translate('Settings', 'Impresora', None)
        )
        self.lbl_printer.setText(
            QCoreApplication.translate('Settings', 'Impresora', None)
        )
        # if QT_CONFIG(tooltip)
        self.cmb_printer.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'Impresora instalada en Windows donde sale la factura al guardar',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.lbl_printer_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_printer_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        # if QT_CONFIG(tooltip)
        self.chk_printer_simulate.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'Encendido: al guardar se muestra la factura en pantalla como saldr\u00eda impresa, sin mandarla a la impresora.',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.chk_printer_simulate.setText(
            QCoreApplication.translate(
                'Settings', 'Simular impresora (mostrar la factura en pantalla)', None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lbl_printer_simulate_source.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'De d\u00f3nde se lee: Sistema (variable de entorno) o .env (archivo junto al programa)',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_printer_simulate_source.setText(
            QCoreApplication.translate('Settings', '.env', None)
        )
        # if QT_CONFIG(tooltip)
        self.push_test_printer.setToolTip(
            QCoreApplication.translate(
                'Settings',
                'Imprime (o muestra, con Simular impresora) una factura de ejemplo',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.push_test_printer.setText(
            QCoreApplication.translate('Settings', 'Probar impresora', None)
        )
        self.lbl_status.setText('')
        self.push_test.setText(
            QCoreApplication.translate('Settings', 'Probar conexi\u00f3n', None)
        )
        self.push_save.setText(QCoreApplication.translate('Settings', 'Guardar', None))
        self.push_cancel.setText(QCoreApplication.translate('Settings', 'Cancelar', None))

    # retranslateUi
