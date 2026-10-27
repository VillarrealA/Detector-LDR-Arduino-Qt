/*
  Instrumentación Biomédica — práctica LDR

  Circuito LDR: +5 V -- LDR -- A0 -- resistencia 10 kOhm -- GND
  LED de interés: D8 -- resistencia 330 Ohm -- ánodo LED; cátodo -- GND
  Tierra común. Luz interferente: linterna o segundo LED independiente.

  Protocolo:
    Orden desde PC '1' enciende LED, '0' apaga LED.
    Arduino transmite cada 100 ms: estado_LED,lectura_A0\n
    Ejemplo: 1,684
  El estado del LED es la REFERENCIA programada; la decisión corresponde
  a Qt a partir del valor de la LDR. No usar LDR para definir la referencia.
*/

const byte PIN_LDR = A0;
const byte PIN_LED = 8;
const unsigned long PERIODO_MS = 100;

bool ledEncendido = false;
unsigned long ultimoEnvio = 0;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  Serial.begin(115200);
  analogReadResolution(10); // UNO: la resolución se fija en 10 bits para usar rango 0--1023.
}

void loop() {
  while (Serial.available() > 0) {
    char orden = Serial.read();
    if (orden == '1') ledEncendido = true;
    if (orden == '0') ledEncendido = false;
    digitalWrite(PIN_LED, ledEncendido ? HIGH : LOW);
  }

  if (millis() - ultimoEnvio >= PERIODO_MS) {
    ultimoEnvio = millis();
    int adc = analogRead(PIN_LDR);
    Serial.print(ledEncendido ? 1 : 0);
    Serial.print(',');
    Serial.println(adc);
  }
}
