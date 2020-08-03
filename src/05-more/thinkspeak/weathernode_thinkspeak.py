from network import WLAN, STA_IF
from machine import Pin
from dht import DHT11
import urequests
import utime
import secrets


THINGSPEAK_REQUEST = 'https://api.thingspeak.com/update?api_key={api_key}&field1={temperature}&field2={humidity}&field3={location}'
PUBLISH_PERIOD_IN_SEC = 60


def connect(wifi):
    wifi = WLAN(STA_IF)
    
    if wifi.isconnected():
        return True

    sleep = utime.sleep

    try:
        wifi.connect(secrets.wifi_network, secrets.wifi_password)
        sleep = utime.sleep

        while not wifi.isconnected():
            print('.')
            sleep(.5)

        print('Connected')
        return True
    except:
        print('Failed to connect to WiFi')
        return False

def run():
    sleep = utime.sleep
    dhtPin = Pin(2, Pin.IN, Pin.PULL_UP)
    sensor = DHT11(dhtPin)
    measure = sensor.measure
    temp = sensor.temperature
    hum = sensor.humidity
    httpget = urequests.get

    wifi = WLAN(STA_IF)

    if not wifi.active():
        wifi.active(True)

    while True:
        if not connect(wifi):
            return

        try:
            measure()
            t = temp() * 1.8 + 32
            h = hum()

            print(t, h)
            httpget(THINGSPEAK_REQUEST.format(temperature=t,
                                              humidity=h,
                                              location='livingroom',
                                              api_key=secrets.THINKSPEAK_API_KEY))
        except:
            print('Failed to read sensor')

        sleep(PUBLISH_PERIOD_IN_SEC)

run()
