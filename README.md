# Detector óptico LED–LDR: adquisición, curvas ROC y precisión–recall

**Instrumentación Biomédica | Práctica con Arduino Mega y Python**

En esta práctica se construye un detector óptico que intenta identificar si un LED está encendido mediante la lectura de una fotorresistencia (LDR). Primero se adquieren datos con el sensor sin protección óptica (**diseño A**); después se añade un capuchón o tubo opaco (**diseño B**) para intentar reducir el efecto de la luz ambiental. Se comparan ambos diseños mediante matrices de confusión, curvas ROC, curvas precisión–recall y criterios de selección de umbral.

El capuchón es una **hipótesis de mejora**, no una garantía. El objetivo es comprobar con mediciones si la modificación aumenta la capacidad del detector para separar las dos clases.

## Objetivos

- Adquirir lecturas ADC de un detector LED–LDR y registrar una referencia conocida.
- Diferenciar el estado real del LED de la decisión que produce el detector.
- Construir e interpretar sensibilidad, especificidad y matriz de confusión.
- Comparar curvas ROC y PR para dos configuraciones físicas.
- Calcular e interpretar AUC ROC, average precision (AP) e índice de Youden.
- Seleccionar y justificar un umbral de operación sin confundirlo con el AUC.

## Archivos

```text
Detector-LDR-Arduino-Qt/
├── README.md
└── Practica_LDR/
    ├── ldr_arduino/
    │   └── ldr_arduino.ino
    ├── app_ldr.py
    ├── ldr.ui
    ├── ui_ldr.py
    ├── analizar_ldr_roc.py
    ├── comparar_diseno_ldr.py
    └── datos_simulados/
        ├── diseno_A_SIMULADO.csv
        └── diseno_B_SIMULADO.csv
```

| Archivo | Función |
| --- | --- |
| `ldr_arduino/ldr_arduino.ino` | Controla el LED (D8), lee el LDR (A0) y transmite datos por puerto serie. |
| `ldr.ui` | Diseño editable de la interfaz en Qt Designer. |
| `ui_ldr.py` | Código de interfaz generado con `pyside6-uic`. Si no está incluido, se puede regenerar. |
| `app_ldr.py` | Interfaz gráfica para adquirir ensayos y exportarlos a CSV. |
| `analizar_ldr_roc.py` | Analiza un diseño: distribución ADC, ROC, PR, AUC, AP y tabla de umbrales. |
| `comparar_diseno_ldr.py` | Compara los archivos de ambos diseños. |
| `datos_simulados/*.csv` | Datos **ficticios**, 32 ensayos por diseño, para practicar o utilizarlos como respaldo. |

## Materiales

- Arduino **Mega 2560**, cable USB y computadora.
- LED y resistencia de **330 Ω**.
- LDR y resistencia de **10 kΩ**.
- Protoboard y cables.
- Linterna u otra fuente luminosa independiente, para generar interferencia.
- Material opaco para el capuchón o tubo de protección.

## Conexiones

```text
+5 V ── LDR ──┬── A0 (Arduino Mega)
              │
             10 kΩ
              │
             GND

D8 ── 330 Ω ── ánodo del LED
               cátodo ── GND
```

Con este divisor, las cuentas ADC aumentan al aumentar la iluminación. El **Arduino Mega mide 0–1023 (10 bits)** con `analogRead(A0)`; **no** utilicen `analogReadResolution(10)` en el sketch para Mega.

## Preparación del software

Instalar Python y las dependencias:

```bash
python -m pip install PySide6 pyserial numpy matplotlib
```

En Arduino IDE, seleccionar **Arduino Mega or Mega 2560**, elegir el puerto COM y cargar `Practica_LDR/ldr_arduino/ldr_arduino.ino`. Cerrar el monitor serie antes de utilizar la interfaz.

Para modificar el diseño Qt (opcional), desde `Practica_LDR/`:

```bash
pyside6-uic ldr.ui -o ui_ldr.py
```

Para ejecutar la interfaz, desde `Practica_LDR/`:

```bash
python app_ldr.py
```

Si se trabaja desde Spyder, es recomendable ejecutar la aplicación Qt desde una terminal para evitar instancias duplicadas de `QApplication`.

## Adquisición: dos diseños

**Diseño A — Sin capuchón.** Realizar 32 ensayos: 16 con el LED encendido (`led_referencia=1`) y 16 apagado (`led_referencia=0`). Incluir condiciones de señal intensa/débil y poca/mucha iluminación interferente, siguiendo las indicaciones del profesor. Exportar el CSV desde `app_ldr.py` y guardarlo como `diseno_A.csv`.

**Diseño B — Con capuchón.** Colocar la protección óptica y repetir otros 32 ensayos siguiendo el mismo protocolo, procurando mantener las condiciones comparables. Guardar el archivo como `diseno_B.csv`.

**Importante:** el estado del LED es la referencia experimental; la lectura del LDR no debe utilizarse para inventar o modificar las etiquetas reales. Registrar un ensayo por condición definida y no presentar mediciones consecutivas como ensayos independientes sin justificación. No alterar datos reales para producir una mejora artificial.

## Formato de los datos

La interfaz guarda columnas como:

```csv
ensayo,hora,led_referencia,adc_ldr,umbral_adc,decision_detectado,categoria
```

Para construir las curvas se usan principalmente **`led_referencia`** (estado real) y **`adc_ldr`** (lectura). El umbral guardado durante la adquisición no limita los umbrales que pueden explorarse posteriormente al calcular una ROC o PR.

En `datos_simulados/` hay archivos claramente identificados como **SIMULADOS**, para quienes necesiten practicar el análisis si la adquisición real falla. No deben describirse como mediciones obtenidas en el laboratorio.

## Análisis individual

Abrir una terminal dentro de `Practica_LDR/` y ejecutar:

```bash
python analizar_ldr_roc.py diseno_A.csv --salida resultados_A
python analizar_ldr_roc.py diseno_B.csv --salida resultados_B
```

Para trabajar con los archivos de respaldo:

```bash
python analizar_ldr_roc.py datos_simulados/diseno_A_SIMULADO.csv --salida resultados_A_simulados
python analizar_ldr_roc.py datos_simulados/diseno_B_SIMULADO.csv --salida resultados_B_simulados
```

Cada ejecución genera la distribución ADC, la curva ROC, la curva PR y `tabla_umbrales.csv`. La regla de decisión es **detectado si `ADC > umbral`**.

**Compatibilidad con NumPy:** si aparece `AttributeError: module 'numpy' has no attribute 'trapezoid'`, reemplazar `np.trapezoid(...)` por `np.trapz(...)` en versiones anteriores a NumPy 2.0; alternativamente, usar una selección compatible con ambas versiones.

## Comparación de ambos diseños

Con los CSV experimentales:

```bash
python comparar_diseno_ldr.py diseno_A.csv diseno_B.csv
```

Con los datos simulados:

```bash
python comparar_diseno_ldr.py datos_simulados/diseno_A_SIMULADO.csv datos_simulados/diseno_B_SIMULADO.csv
```

*Estos comandos suponen que `comparar_diseno_ldr.py` acepta dos rutas posicionales. Si la versión distribuida tiene opciones adicionales, revisar `python comparar_diseno_ldr.py --help`.*

Comparar como mínimo:

- Distribución de ADC para LED encendido y apagado.
- Curvas ROC y sus AUC.
- Curvas precisión–recall y sus AP.
- Máximo índice de Youden, `J = sensibilidad + especificidad - 1`.
- Umbral de operación propuesto para cada diseño, justificando los errores que se desean evitar.

Un mayor AUC o AP indica mejor discriminación en los datos evaluados, **no** que cualquier umbral sea adecuado. Un umbral seleccionado con un conjunto de datos debe probarse, idealmente, con ensayos nuevos e independientes.

## Entregables sugeridos

1. Archivos CSV originales de ambos diseños, o indicación explícita de que se utilizaron los simulados.
2. Gráficas ROC y PR comparativas, más las distribuciones ADC.
3. Tabla con AUC, AP y máximo índice de Youden por diseño.
4. Umbral elegido para cada configuración, acompañado de sensibilidad, especificidad y precisión.
5. Conclusión breve: ¿el capuchón mejoró realmente el detector?, ¿qué evidencia lo respalda?, ¿qué limitaciones tiene el experimento?

**Curso:** Instrumentación Biomédica. Material didáctico; el detector LED–LDR es una analogía para estudiar evaluación instrumental, no un dispositivo de diagnóstico clínico.
