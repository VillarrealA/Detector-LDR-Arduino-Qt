# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ldr.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(740, 530)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setAlignment(Qt.AlignCenter)
        self.labelTitulo.setStyleSheet(u"font-size: 19px; font-weight: bold; color: #12345A;")

        self.verticalLayout.addWidget(self.labelTitulo)

        self.horizontalLayoutPort = QHBoxLayout()
        self.horizontalLayoutPort.setObjectName(u"horizontalLayoutPort")
        self.labelPuerto = QLabel(self.centralwidget)
        self.labelPuerto.setObjectName(u"labelPuerto")

        self.horizontalLayoutPort.addWidget(self.labelPuerto)

        self.comboPuerto = QComboBox(self.centralwidget)
        self.comboPuerto.setObjectName(u"comboPuerto")

        self.horizontalLayoutPort.addWidget(self.comboPuerto)

        self.btnActualizar = QPushButton(self.centralwidget)
        self.btnActualizar.setObjectName(u"btnActualizar")

        self.horizontalLayoutPort.addWidget(self.btnActualizar)

        self.btnConectar = QPushButton(self.centralwidget)
        self.btnConectar.setObjectName(u"btnConectar")

        self.horizontalLayoutPort.addWidget(self.btnConectar)


        self.verticalLayout.addLayout(self.horizontalLayoutPort)

        self.labelConexion = QLabel(self.centralwidget)
        self.labelConexion.setObjectName(u"labelConexion")
        self.labelConexion.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labelConexion)

        self.horizontalLayoutDatos = QHBoxLayout()
        self.horizontalLayoutDatos.setObjectName(u"horizontalLayoutDatos")
        self.grupoReferencia = QGroupBox(self.centralwidget)
        self.grupoReferencia.setObjectName(u"grupoReferencia")
        self.verticalLayoutRef = QVBoxLayout(self.grupoReferencia)
        self.verticalLayoutRef.setObjectName(u"verticalLayoutRef")
        self.labelReferencia = QLabel(self.grupoReferencia)
        self.labelReferencia.setObjectName(u"labelReferencia")
        self.labelReferencia.setAlignment(Qt.AlignCenter)
        self.labelReferencia.setStyleSheet(u"font-size: 23px; font-weight: bold;")

        self.verticalLayoutRef.addWidget(self.labelReferencia)

        self.btnLed = QPushButton(self.grupoReferencia)
        self.btnLed.setObjectName(u"btnLed")
        self.btnLed.setEnabled(False)

        self.verticalLayoutRef.addWidget(self.btnLed)


        self.horizontalLayoutDatos.addWidget(self.grupoReferencia)

        self.grupoMedicion = QGroupBox(self.centralwidget)
        self.grupoMedicion.setObjectName(u"grupoMedicion")
        self.verticalLayoutMed = QVBoxLayout(self.grupoMedicion)
        self.verticalLayoutMed.setObjectName(u"verticalLayoutMed")
        self.labelMedicion = QLabel(self.grupoMedicion)
        self.labelMedicion.setObjectName(u"labelMedicion")
        self.labelMedicion.setAlignment(Qt.AlignCenter)
        self.labelMedicion.setStyleSheet(u"font-size: 30px; font-weight: bold; color: #12345A;")

        self.verticalLayoutMed.addWidget(self.labelMedicion)

        self.horizontalLayoutUmbral = QHBoxLayout()
        self.horizontalLayoutUmbral.setObjectName(u"horizontalLayoutUmbral")
        self.labelUmbral = QLabel(self.grupoMedicion)
        self.labelUmbral.setObjectName(u"labelUmbral")

        self.horizontalLayoutUmbral.addWidget(self.labelUmbral)

        self.spinUmbral = QSpinBox(self.grupoMedicion)
        self.spinUmbral.setObjectName(u"spinUmbral")
        self.spinUmbral.setMaximum(1023)
        self.spinUmbral.setValue(500)

        self.horizontalLayoutUmbral.addWidget(self.spinUmbral)


        self.verticalLayoutMed.addLayout(self.horizontalLayoutUmbral)


        self.horizontalLayoutDatos.addWidget(self.grupoMedicion)


        self.verticalLayout.addLayout(self.horizontalLayoutDatos)

        self.grupoDecision = QGroupBox(self.centralwidget)
        self.grupoDecision.setObjectName(u"grupoDecision")
        self.verticalLayoutDecision = QVBoxLayout(self.grupoDecision)
        self.verticalLayoutDecision.setObjectName(u"verticalLayoutDecision")
        self.labelDecision = QLabel(self.grupoDecision)
        self.labelDecision.setObjectName(u"labelDecision")
        self.labelDecision.setAlignment(Qt.AlignCenter)
        self.labelDecision.setMinimumSize(QSize(0, 68))
        self.labelDecision.setStyleSheet(u"font-size: 28px; font-weight: bold; background: #EAF1F8; border-radius: 7px; color: #12345A;")

        self.verticalLayoutDecision.addWidget(self.labelDecision)


        self.verticalLayout.addWidget(self.grupoDecision)

        self.horizontalLayoutAcciones = QHBoxLayout()
        self.horizontalLayoutAcciones.setObjectName(u"horizontalLayoutAcciones")
        self.btnEvaluar = QPushButton(self.centralwidget)
        self.btnEvaluar.setObjectName(u"btnEvaluar")
        self.btnEvaluar.setEnabled(False)

        self.horizontalLayoutAcciones.addWidget(self.btnEvaluar)

        self.btnRegistrar = QPushButton(self.centralwidget)
        self.btnRegistrar.setObjectName(u"btnRegistrar")
        self.btnRegistrar.setEnabled(False)

        self.horizontalLayoutAcciones.addWidget(self.btnRegistrar)

        self.btnFinalizar = QPushButton(self.centralwidget)
        self.btnFinalizar.setObjectName(u"btnFinalizar")
        self.btnFinalizar.setEnabled(False)

        self.horizontalLayoutAcciones.addWidget(self.btnFinalizar)


        self.verticalLayout.addLayout(self.horizontalLayoutAcciones)

        self.labelModo = QLabel(self.centralwidget)
        self.labelModo.setObjectName(u"labelModo")

        self.verticalLayout.addWidget(self.labelModo)

        self.labelConteos = QLabel(self.centralwidget)
        self.labelConteos.setObjectName(u"labelConteos")
        self.labelConteos.setAlignment(Qt.AlignCenter)
        self.labelConteos.setStyleSheet(u"font-size: 15px; font-weight: bold;")

        self.verticalLayout.addWidget(self.labelConteos)

        self.labelArchivo = QLabel(self.centralwidget)
        self.labelArchivo.setObjectName(u"labelArchivo")
        self.labelArchivo.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelArchivo)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Instrumentaci\u00f3n Biom\u00e9dica | Detector \u00f3ptico LDR", None))
        self.labelTitulo.setText(QCoreApplication.translate("MainWindow", u"Detecci\u00f3n de una fuente luminosa mediante LDR", None))
        self.labelPuerto.setText(QCoreApplication.translate("MainWindow", u"Puerto:", None))
        self.btnActualizar.setText(QCoreApplication.translate("MainWindow", u"Actualizar", None))
        self.btnConectar.setText(QCoreApplication.translate("MainWindow", u"Conectar", None))
        self.labelConexion.setText(QCoreApplication.translate("MainWindow", u"Sin conexi\u00f3n", None))
        self.grupoReferencia.setTitle(QCoreApplication.translate("MainWindow", u"Referencia: LED de inter\u00e9s", None))
        self.labelReferencia.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.btnLed.setText(QCoreApplication.translate("MainWindow", u"Encender LED", None))
        self.grupoMedicion.setTitle(QCoreApplication.translate("MainWindow", u"Lectura de la LDR (ADC)", None))
        self.labelMedicion.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.labelUmbral.setText(QCoreApplication.translate("MainWindow", u"Umbral ADC:", None))
        self.grupoDecision.setTitle(QCoreApplication.translate("MainWindow", u"Decisi\u00f3n del detector (no es la referencia)", None))
        self.labelDecision.setText(QCoreApplication.translate("MainWindow", u"SIN DATOS", None))
        self.btnEvaluar.setText(QCoreApplication.translate("MainWindow", u"Iniciar evaluaci\u00f3n (fijar umbral)", None))
        self.btnRegistrar.setText(QCoreApplication.translate("MainWindow", u"Registrar ensayo", None))
        self.btnFinalizar.setText(QCoreApplication.translate("MainWindow", u"Finalizar evaluaci\u00f3n", None))
        self.labelModo.setText(QCoreApplication.translate("MainWindow", u"Modo: calibraci\u00f3n (puede cambiar el umbral)", None))
        self.labelConteos.setText(QCoreApplication.translate("MainWindow", u"VP: 0     FN: 0     FP: 0     VN: 0", None))
        self.labelArchivo.setText(QCoreApplication.translate("MainWindow", u"Los ensayos registrados se guardar\u00e1n en CSV.", None))
    # retranslateUi

