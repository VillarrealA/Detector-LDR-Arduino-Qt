"""Interfaz mínima para práctica LDR, diseñada con Qt Designer.

Arduino envía por USB: estado_real_LED,ADC\n (ej. 1,684).
La decisión se toma aquí: ADC > umbral => DETECTADO.
El botón Registrar ensayo guarda un evento y su referencia en CSV.

Antes de ejecutar:
  pyside6-uic ldr.ui -o ui_ldr.py
  python app_ldr.py
"""

import csv
from datetime import datetime
from pathlib import Path
import sys
import time

import serial
from serial.tools import list_ports
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui_ldr import Ui_MainWindow  # Archivo generado desde Qt Designer


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.puerto = None
        self.buffer = b""
        self.referencia = None  # Estado del LED enviado por Arduino: 0/1
        self.adc = None         # Medición cruda de la LDR: 0..1023
        self.ultimo_dato = 0.0
        self.ultimo_cambio_led = 0.0
        self.led_solicitado = None
        self.evaluando = False
        self.archivo = None
        self.ensayo = 0
        self.conteos = {"VP": 0, "FN": 0, "FP": 0, "VN": 0}

        self.ui.btnActualizar.clicked.connect(self.buscar_puertos)
        self.ui.btnConectar.clicked.connect(self.conectar)
        self.ui.btnLed.clicked.connect(self.cambiar_led)
        self.ui.btnEvaluar.clicked.connect(self.iniciar_evaluacion)
        self.ui.btnRegistrar.clicked.connect(self.registrar_ensayo)
        self.ui.btnFinalizar.clicked.connect(self.finalizar_evaluacion)
        self.ui.spinUmbral.valueChanged.connect(self.mostrar_decision)

        self.temporizador = QTimer(self)
        self.temporizador.timeout.connect(self.leer_serial)
        self.temporizador.start(100)  # Se actualiza sin bloquear la ventana.
        self.buscar_puertos()

    def buscar_puertos(self):
        disponibles = [p.device for p in list_ports.comports()]
        self.ui.comboPuerto.clear()
        self.ui.comboPuerto.addItems(disponibles)
        if "COM3" in disponibles:  # Puerto usado en las pruebas anteriores; opcional.
            self.ui.comboPuerto.setCurrentText("COM3")

    def conectar(self):
        if self.puerto is not None:
            if self.evaluando:
                self.finalizar_evaluacion()
            self.puerto.close()
            self.puerto = None
            self.referencia = None
            self.adc = None
            self.ui.btnConectar.setText("Conectar")
            self.ui.btnLed.setEnabled(False)
            self.ui.btnEvaluar.setEnabled(False)
            self.ui.btnRegistrar.setEnabled(False)
            self.ui.labelConexion.setText("Sin conexión")
            self.mostrar_decision()
            return

        nombre = self.ui.comboPuerto.currentText()
        if not nombre:
            QMessageBox.warning(self, "Puerto", "No se encontró ningún puerto serie.")
            return
        try:
            self.puerto = serial.Serial(nombre, 115200, timeout=0)
        except serial.SerialException as exc:
            QMessageBox.critical(self, "Puerto ocupado", str(exc))
            return
        self.buffer = b""
        self.referencia = None
        self.adc = None
        self.ui.btnConectar.setText("Desconectar")
        self.ui.btnLed.setEnabled(True)
        self.ui.btnEvaluar.setEnabled(True)
        self.ui.labelConexion.setText(f"Conectado a {nombre}; esperando datos...")

    def cambiar_led(self):
        if self.puerto is None or self.referencia is None:
            return
        nuevo_estado = 0 if self.referencia else 1
        try:
            self.puerto.write(b"1" if nuevo_estado else b"0")
        except serial.SerialException as exc:
            self.ui.labelConexion.setText(f"Error de escritura: {exc}")
            return
        self.led_solicitado = nuevo_estado
        self.ultimo_cambio_led = time.monotonic()
        self.ui.btnRegistrar.setEnabled(False)  # Esperar cambio y estabilización.

    def leer_serial(self):
        if self.puerto is None:
            return
        try:
            cantidad = self.puerto.in_waiting
            if cantidad:
                self.buffer += self.puerto.read(cantidad)
                # Evita crecimiento ilimitado ante datos corruptos.
                if len(self.buffer) > 4096:
                    self.buffer = self.buffer[-4096:]
                while b"\n" in self.buffer:
                    linea, self.buffer = self.buffer.split(b"\n", 1)
                    try:
                        estado_texto, adc_texto = linea.strip().decode("ascii").split(",")
                        estado, adc = int(estado_texto), int(adc_texto)
                    except (ValueError, UnicodeDecodeError):
                        continue
                    if estado not in (0, 1) or not (0 <= adc <= 1023):
                        continue
                    self.referencia, self.adc = estado, adc
                    self.ultimo_dato = time.monotonic()
        except (serial.SerialException, OSError) as exc:
            self.ui.labelConexion.setText(f"Se perdió la conexión: {exc}")
            self.puerto.close()
            self.puerto = None
            self.ui.btnLed.setEnabled(False)
            self.ui.btnEvaluar.setEnabled(False)
            self.ui.btnRegistrar.setEnabled(False)
            return

        if self.adc is not None:
            self.ui.labelMedicion.setText(str(self.adc))
            self.ui.labelReferencia.setText("ENCENDIDO" if self.referencia else "APAGADO")
            self.ui.btnLed.setText("Apagar LED" if self.referencia else "Encender LED")
            self.ui.labelConexion.setText("Recibiendo datos del Arduino")
        self.mostrar_decision()

        ya_estable = time.monotonic() - self.ultimo_cambio_led >= 0.7
        estado_confirmado = self.led_solicitado is None or self.referencia == self.led_solicitado
        dato_reciente = time.monotonic() - self.ultimo_dato < 0.5
        self.ui.btnRegistrar.setEnabled(
            self.evaluando and self.adc is not None
            and ya_estable and estado_confirmado and dato_reciente
        )

    def mostrar_decision(self, _=None):
        if self.adc is None:
            texto, fondo, color = "SIN DATOS", "#EAF1F8", "#12345A"
        elif self.adc > self.ui.spinUmbral.value():
            texto, fondo, color = "DETECTADO", "#D9F3E4", "#145C35"
        else:
            texto, fondo, color = "NO DETECTADO", "#F8E1E1", "#802727"
        self.ui.labelDecision.setText(texto)
        self.ui.labelDecision.setStyleSheet(
            f"font-size:28px; font-weight:bold; background:{fondo};"
            f"border-radius:7px; color:{color};"
        )

    def iniciar_evaluacion(self):
        if self.puerto is None or self.adc is None:
            QMessageBox.warning(self, "Adquisición", "Primero conecte el Arduino y espere una lectura.")
            return
        self.ensayo = 0
        self.conteos = {"VP": 0, "FN": 0, "FP": 0, "VN": 0}
        nombre = "ensayos_ldr_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        self.archivo = Path(__file__).resolve().parent / nombre
        with self.archivo.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "ensayo", "hora", "led_referencia", "adc_ldr", "umbral_adc",
                "decision_detectado", "categoria"
            ])
        self.evaluando = True
        self.ui.spinUmbral.setEnabled(False)  # Criterio fijado antes de evaluar.
        self.ui.btnEvaluar.setEnabled(False)
        self.ui.btnFinalizar.setEnabled(True)
        self.ui.labelModo.setText("Modo: EVALUACIÓN (umbral bloqueado)")
        self.ui.labelArchivo.setText(f"Guardando ensayos en: {self.archivo.name}")
        self.actualizar_conteos()

    def registrar_ensayo(self):
        if not self.evaluando or self.referencia is None or self.adc is None:
            return
        if time.monotonic() - self.ultimo_dato > 0.5:
            return
        if time.monotonic() - self.ultimo_cambio_led < 0.7:
            return
        if self.led_solicitado is not None and self.referencia != self.led_solicitado:
            return

        detectado = int(self.adc > self.ui.spinUmbral.value())
        caso = ("VP" if detectado else "FN") if self.referencia else ("FP" if detectado else "VN")
        self.conteos[caso] += 1
        self.ensayo += 1
        with self.archivo.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                self.ensayo, datetime.now().isoformat(timespec="seconds"),
                self.referencia, self.adc, self.ui.spinUmbral.value(), detectado, caso
            ])
        self.actualizar_conteos()
        self.ui.statusbar.showMessage(f"Ensayo {self.ensayo}: {caso}", 3000)

    def actualizar_conteos(self):
        c = self.conteos
        self.ui.labelConteos.setText(
            f"Ensayos: {self.ensayo}     VP: {c['VP']}     FN: {c['FN']}"
            f"     FP: {c['FP']}     VN: {c['VN']}"
        )

    def finalizar_evaluacion(self):
        self.evaluando = False
        self.ui.spinUmbral.setEnabled(True)
        self.ui.btnRegistrar.setEnabled(False)
        self.ui.btnEvaluar.setEnabled(self.puerto is not None)
        self.ui.btnFinalizar.setEnabled(False)
        self.ui.labelModo.setText("Modo: calibración (puede cambiar el umbral)")
        self.ui.statusbar.showMessage("Evaluación finalizada; CSV guardado.", 6000)

    def closeEvent(self, event):
        if self.puerto is not None:
            try:
                self.puerto.write(b"0")  # Intentar dejar el LED apagado.
                self.puerto.close()
            except (serial.SerialException, OSError):
                pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
