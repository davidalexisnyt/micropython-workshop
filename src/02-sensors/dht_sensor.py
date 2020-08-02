"""
    --------------------------------------------------------------------------------------
    dhtSensor.py
    --------------------------------------------------------------------------------------

    This script shows hot to use the DHT11/22 digital humidity and temperature sensors.
    These sensors cost around $3 or $4.

    The sensor provides temperature values in Celcius, which can then be easily converted
    to Fahrenheit if needed.  The sensors can only read measurements every 2 seconds, so
    a delay needs to be inserted between readings.

    Author:  David Alexis (2019)
    --------------------------------------------------------------------------------------
"""

from machine import Pin
from time import sleep
import dht


SENSOR_PIN = 5


def main():
    sensor = dht.DHT22(Pin(SENSOR_PIN))
    # sensor = dht.DHT11(Pin(SENSOR_PIN))   # <-- Use this line if you have a DHT11 sensor.

    while True:
        # Get sensor readings
        # The measure() method actually samples the temperature and humidity, and stores
        # the values internally. The values are then accessed by calling temperature()
        # and humidity().
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Temperature is returned in Celcius. Let's convert to Fahrenheit.
        temperatureF = (temperature * 1.8 + 32)

        reading = {
            "temperature_F": int(temperatureF),
            "humidity": int(humidity)
        }

        print(reading)

        # Wait at least 2 seconds before next reading, since the DHT sensor's measure() methos
        # can only be called once every 2 seconds.
        sleep(5)


# ----- Program starts here -----
main()
