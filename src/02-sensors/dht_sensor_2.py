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
import dht
from time import sleep


SENSOR_PIN = 5


def main():
    pin = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    sensor = dht.DHT22(pin)
    # sensor = dht.DHT11(pin)   # <-- Use this line if you have a DHT11 sensor.

    while True:
        try:
            try:
                sensor.measure()
                temperature = sensor.temperature()
                humidity = sensor.humidity()

                if isinstance(temperature, float) and isinstance(humidity, float):
                    temperatureF = int((temperature * 1.8 + 32))

                    reading = {
                        "temperature_F": temperatureF,
                        "humidity": humidity
                    }

                    print(reading)
                else:
                    print("Could not get reading")
            except OSError:
                print("Sensor failed")

            # Wait at least 2 seconds before next reading, since the DHT sensor's measure() methos
            # can only be called once every 2 seconds.
            sleep(5)
        except KeyboardInterrupt:
            print("Bye")
            break


# ----- Program starts here -----
main()
