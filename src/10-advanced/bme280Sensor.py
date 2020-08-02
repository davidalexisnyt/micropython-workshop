from machine import Pin, I2C
from utime import sleep
from lib.bme280 import BME280
import ssd1306


scl = Pin(5, Pin.PULL_UP)
sda = Pin(4, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=10000)
bme = BME280(i2c=i2c)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

while True:
    try:
        # temp = round(bme.temperature() * 1.8 + 32)
        # hum = round(bme.humidity())
        # pres = bme.pressure()
        temp, hum, pres = bme.measure(temperature_unit='F')

        display.fill(0)
        display.text("T: {}F H: {}%".format(temp, hum), 0, 3, 1)
        display.text("P: {}hPa".format(pres), 0, 20, 1)
        display.show()

        msg = "{" + " 'node': 'dalexis-sensor1', 'temperature_F': {}, 'humidity': {}, 'pressure': {} ".format(temp, hum, pres) + "}"
        print(msg)

        sleep(10)
    except KeyboardInterrupt:
        print("Bye")
        break
