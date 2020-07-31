# raspberry-sensor-cjmcu-3935

Este repositorio está almacenado en gitlab:
https://gitlab.com/fryntiz/raspberry-sensor-cjmcu-3935

Repositorio para controlar por i2c el sensor CJMCU 3935 con el chip AS3935.
Este chip se utiliza para detectar rayos y la distancia de estos.

Este proyecto está escrito en python 3.7, por lo que no funcionará en una
versión anterior a la **3** y no se garantiza que funcione correctamente en
una versión anterior a la **3.7**

La versión del sistema operativo en la raspberry pi es raspbian 10 stable.

## Sensor AS3935

La caída de rayos produce descargas electrostáticas y este sensor reacciona al
alto potencial eléctrico de estas.

Se producen por tormentas eléctricas cargadas negativamente que caen a la tierra
principalmente (75-90% de probabilidad) pero también de nube a nube.

La corriente cambia rápidamente al sentir el pulso electromagnético (10-150ms)
en la VLF (3k-30 kHz) y las bandas de radios ELF (<3 kHz)

The maximum amplitude lies around 5-10KHz.

El algoritmo de detección no modificable en el AS3935 está preparado para
una señal de 500kHz.

## Dependencias desde pip

Utilizando el gestor de paquetes pip para python 3 instalamos las dependencias:

```bash
pip3 install RPi_AS3935
```

## Detalles

Antes de usar el ejemplo es necesario tener en cuenta estos detalles o
modificarlos a nuestro uso.

- Está conectado por i2c
- La dirección i2c es 0x03
- El pin por defecto es el GPIO25
- El bus por defecto a partir de Raspberry Pi 2 es comúnmente el **1**, 
para anteriores es necesario cambiarlo a **0**

## Conexión con hardware

Con la siguiente configuración queda la señal de interrupción en el GPIO 25 para tomar los datos desde el script que utilicemos.
De esta forma además, la dirección será 0x03.

VCC → 3.3V
GND → GND
MOSI → PIN 3
SCL → PIN 5
SI → 3.3V
A0 → 3.3V
A1 → 3.3V
IRQ → GPIO 25, este recibe la señal de interrupción al detectar algo.

## Usar ejemplo

Para ejecutar el script de ejemplo adjunto en el repositorio y comprobar
el funcionamiento del sensor y código ejecutamos el archivo example.py con
el intérprete para python 3.

```bash
python3 example.py
```