





# Optimizations





# Snippets



```python
from machine import Pin
import dht
import utime

dhtPin = Pin(5, Pin.IN, Pin.PULL_UP)
dht11 = dht.DHT11(dhtPin)

def run():
    measure = dht11.measure
    temp = dht11.temperature
    hum = dht11.humidity
    sleep = utime.sleep

    while True:
        try:
            measure()
            tC = temp()
            tF = (tC * 1.8) + 32
            h = hum()
            print(tF, " - ", h)
        except:
            print('bad reading')

    sleep(5)

run()
```



```python
import network
from machine import Pin, I2C
import ssd1306
import dht
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

import secrets


MAX_ATTEMPTS = 20
attempt_count = 0

client_id = "unit1"
mqtt_feedname = b'sensors/temp'
PUBLISH_PERIOD_IN_SEC = 10


def connect_wifi():
    """
    Wait until the device is connected to the WiFi network
    """
    global attempt_count

    if wifi.isconnected():
        return True

    while wifi.isconnected() == False and attempt_count < MAX_ATTEMPTS:
        print('Connecting to WiFI...')
        attempt_count += 1

        wifi.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

        connection_countdown = 15

        while connection_countdown > 0:
            if wifi.isconnected():
                break

            connection_countdown -= 1
            time.sleep(.5)

        if wifi.isconnected():
            print("Connected to WiFi")
            return True

        if attempt_count < MAX_ATTEMPTS:
            print('Could not connect to the WiFi network.  Trying again.')

            time.sleep(2)
            continue
        else:
            print('Failed to connect to WiFi.  Aborting for now.')
            display.fill(0)
            display.text('Could not connect to', 0, 0)
            display.text('WiFi!', 0, 10)
            display.show()

    return False

def connect_to_mqtt():
    def mqtt_is_connected():
        if mqtt_client is None:
            return False

        try:
            mqtt_client.ping()
            return True
        except:
            return False

    if mqtt_is_connected():
        return True

    try:
        mqtt_client.connect()
        return True
    except Exception as e:
        print('could not connect to MQTT server {} - {}'.format(secrets.MQTT_SERVER, e))
        print(e)
        return False

# -------------------------------------------------------------------------------------------

dhtPin = Pin(2, Pin.IN, Pin.PULL_UP)
sensor = dht.DHT11(dhtPin)

i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.text('Initializing...', 5, 5)
display.show()

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

mqtt_client = MQTTClient(client_id=client_id,
                    server=secrets.MQTT_SERVER,
                    user=secrets.MQTT_USER,
                    password=secrets.MQTT_PASSWORD,
                    ssl=False)

connect_wifi()

display.fill(0)
display.show()

while True:
    # Ensure that we're connected to WiFi
    if not connect_wifi():
        sys.exit()

    try:
        if not connect_to_mqtt():
            wifi.disconnect()
            time.sleep(2)
            continue

        sensor.measure()
        temperatureF = (sensor.temperature() * (9 / 5)) + 32
        temperature = str(round(temperatureF, 2))
        humidity = sensor.humidity()

        display.fill(0)
        display.text('Temp:     {}'.format(temperature), 5, 5)
        display.text('Humidity: {}'.format(humidity), 5, 20)
        display.show()

        msg = b'{{ "deviceId": "{}", "tempF": "{}", "humidity": {} }}'.format(
                client_id,
                temperature,
                humidity)

        mqtt_client.publish(mqtt_feedname, msg, qos=0)
        print('Temp: {}  Hum: {}'.format(temperature, humidity))
        mqtt_client.disconnect()

        time.sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting', 0, 0)
        mqtt_client.disconnect()
        sys.exit()
    except Exception as e:
        display.fill(0)
        display.text("Something failed: {}".format(e), 0, 0)
        display.show()

        print(e)
        time.sleep(10)
```



```python
from machine import I2C, Pin
import ssd1306

i2c = I2C(-1, Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# ICON = [
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
#     [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
#     [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
#     [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
#     [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
#     [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
# ]
#
# display.fill(0) # Clear the display
# for y, row in enumerate(ICON):
#     for x, c in enumerate(row):
#         display.pixel(x, y, c)
#
# display.text("Hello world!", 20, 3, 1)
# display.show()

import framebuf

# FrameBuffer needs 2 bytes for every RGB565 pixel
fbuf = framebuf.FrameBuffer(bytearray(10 * 100 * 2), 128, 32, framebuf.MONO_HLSB)

fbuf.fill(0)
fbuf.text('MicroPython!', 0, 0, 0xffff)
fbuf.hline(0, 10, 96, 0xffff)

display.blit(fbuf, 0, 0)
display.show()

```



```python
import machine
import time

LED_PIN = 2  # D4
LED2_PIN = 16  # D0
BUTTON_PIN = 14  # D5

def blink():
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    led2 = machine.Pin(LED2_PIN, machine.Pin.OUT)
    button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

    while True:
        while not button.value():
            led.on()
            led2.off()
            time.sleep(0.5)
            led.off()
            led2.on()
            time.sleep(0.5)

        led.on()
        led2.on()

blink()
```



