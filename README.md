# Práctica: detector óptico con LDR y Qt Designer

**Instrumentación Biomédica · Sensibilidad y especificidad**

Esta práctica implementa un detector sencillo que intenta identificar si un **LED de interés está encendido**, aun cuando exista iluminación ambiental o una fuente luminosa interferente. Se adquiere la respuesta de una fotorresistencia (LDR) con Arduino y se visualiza mediante una interfaz gráfica construida con **Qt Designer y PySide6**.

El objetivo no es medir una condición clínica: es evaluar una **decisión de detección** mediante una referencia conocida y construir una matriz de confusión con verdaderos positivos (VP), falsos negativos (FN), falsos positivos (FP) y verdaderos negativos (VN).

## Archivos

| Archivo | Función |
| --- | --- |
| `ldr_arduino.ino` | Controla el LED en D8, lee la LDR en A0 y envía los datos por puerto serie. |
| `ldr.ui` | Diseño editable de la interfaz en Qt Designer. |
| `app_ldr.py` | Interfaz en Python, lectura del puerto serie, decisión de detección y registro CSV. |
| `README.md` | Esta guía. |

## Material necesario

- Arduino (o placa compatible con lectura analógica, ajustando el código si es necesario).
- LDR y resistencia de **10 kΩ**.
- LED de interés y resistencia de **330 Ω**.
- Protoboard, cables y conexión USB.
- Fuente de luz adicional (linterna u otro LED) para introducir interferencia.
- Computadora con Python, PySide6 y pyserial.

## Conexiones

```text
+5 V ── LDR ──┬── A0 (Arduino)
              │
           10 kΩ
              │
             GND

D8 ── 330 Ω ── ánodo del LED
               cátodo ── GND
```

En esta conexión, la lectura de A0 **aumenta al aumentar la iluminación**:

\[
V_{A0}=V_{cc}\frac{10\,\mathrm{k}\Omega}{R_{LDR}+10\,\mathrm{k}\Omega}.
\]

El programa Arduino configura una resolución de **10 bits**: valores ADC entre **0 y 1023**. La luz interferente debe ser independiente del LED controlado por D8.

## Preparación del software (Windows y Conda)

1. Abrir `ldr_arduino.ino` en Arduino IDE, seleccionar la placa y el puerto correspondiente y cargar el programa. **Cerrar el monitor serie** antes de utilizar la interfaz.
2. Abrir una terminal en esta carpeta y activar el entorno:

   ```bash
   conda activate myenv
   python -m pip install PySide6 pyserial
   ```

3. Si se desea editar la interfaz, abrirla en Qt Designer:

   ```bash
   designer ldr.ui
   ```

4. Generar el archivo Python a partir del diseño (este paso se repite si se modifica `ldr.ui`):

   ```bash
   pyside6-uic ldr.ui -o ui_ldr.py
   ```

5. Ejecutar la aplicación:

   ```bash
   python app_ldr.py
   ```

6. Seleccionar el puerto de Arduino (por ejemplo, `COM3`) y pulsar **Conectar**.

> **Nota:** Si Arduino IDE indica que el puerto está ocupado, cerrar `app_ldr.py` y cualquier otro programa que esté utilizando ese puerto. Para evitar problemas con múltiples instancias de `QApplication` en Spyder, se recomienda ejecutar la aplicación desde una terminal.

## Funcionamiento

Arduino transmite aproximadamente cada **100 ms** dos valores separados por coma:

```text
estado_LED,lectura_A0
1,684
0,412
```

- `estado_LED`: **referencia programada** (`1` = encendido, `0` = apagado).
- `lectura_A0`: señal medida con la LDR, de `0` a `1023`.
- La interfaz decide **DETECTADO** cuando `ADC > umbral`; en caso contrario muestra **NO DETECTADO**.

La referencia **no** se obtiene de la LDR: proviene del estado del LED ordenado por Arduino. Antes de iniciar, verificar que el LED físico responda a los comandos.

## Procedimiento de laboratorio

### 1. Exploración y ajuste

- Encender y apagar el LED desde la interfaz.
- Observar los valores ADC con distintas distancias e intensidades de iluminación.
- Introducir luz interferente mientras el LED de interés está apagado.
- Proponer y ajustar un **umbral de detección** usando únicamente estas pruebas preliminares.

### 2. Evaluación experimental

1. Pulsar **Iniciar evaluación**: el umbral queda bloqueado.
2. Realizar ensayos con LED encendido y apagado, incluyendo situaciones fáciles y difíciles de distinguir (por ejemplo, señal débil o interferencia intensa).
3. Esperar a que se estabilice la lectura y pulsar **Registrar ensayo** una sola vez por ensayo definido. La aplicación espera al menos **0.7 s** después de cambiar el LED para habilitar el registro.
4. Completar una cantidad acordada de ensayos positivos y negativos; no repetir lecturas consecutivas de una condición fija como si fueran ensayos independientes.
5. Pulsar **Finalizar evaluación** y conservar el archivo CSV generado.

Las condiciones difíciles favorecen los errores de clasificación, pero **no se deben inventar falsos positivos ni falsos negativos** si no aparecen en los registros reales.

## Interpretación de la matriz de confusión

| Referencia real | Decisión de la interfaz | Categoría |
| --- | --- | --- |
| LED encendido | Detectado | VP |
| LED encendido | No detectado | FN |
| LED apagado | Detectado | FP |
| LED apagado | No detectado | VN |

\[
\mathrm{Sensibilidad}=\frac{VP}{VP+FN},\qquad
\mathrm{Especificidad}=\frac{VN}{VN+FP}.
\]

**Interpretación:** el sistema evalúa la capacidad de identificar el **estado del LED de interés**, no la calidad de una medición clínica.

## Archivos de resultados

La aplicación guarda un archivo con nombre similar a:

```text
ensayos_ldr_20261023_133000.csv
```

Columnas del CSV:

```csv
ensayo,hora,led_referencia,adc_ldr,umbral_adc,decision_detectado,categoria
1,2026-10-23T13:30:00,1,730,500,1,VP
2,2026-10-23T13:30:07,0,680,500,1,FP
```

*Las dos filas anteriores son ejemplos ilustrativos, no mediciones experimentales.*

Guardar los CSV de forma separada para los ensayos de **selección** y **validación** del umbral. Estas mediciones se pueden reutilizar posteriormente para construir curvas **ROC** y **precisión–recall**.

## Recomendaciones

- Mantener la misma geometría de medición durante cada serie de ensayos, salvo cuando esa variable forme parte del protocolo.
- Fijar el umbral **antes** de evaluar los ensayos que se utilizarán para reportar desempeño.
- Registrar las condiciones experimentales que no aparecen en el CSV: distancia, orientación, iluminación ambiental y observaciones.
- Si se desea una evaluación ciega, una persona puede controlar la secuencia de LED y otra interpretar las decisiones sin ver la referencia en pantalla.
- No subir registros que contengan datos personales si más adelante se adapta la práctica para señales fisiológicas.

---

**Curso:** Instrumentación Biomédica · Material didáctico para adquisición de datos, clasificación y evaluación de detectores.
