"""
    --------------------------------------------------------------------------------------
    dht_sensor_mqtt.py
    --------------------------------------------------------------------------------------
    Demonstrates how to connect to a remote MQTT message broker, and send temperature
    and humidity readings to a queue.

    Author:  David Alexis (2020)
    --------------------------------------------------------------------------------------
"""

from machine import Pin
import time
import dht
from umqtt.robust import MQTTClient
import ujson
import secrets

SENSOR_PIN = 5  # Change SENSOR_PIN to match the actual pin the sensor is connected to
TOPIC = 'sensors/environmental'
LOCATION = 'living room'  # Change to describe your device location
READING_INTERVAL_SECONDS = 5


def connect():
    import networkUtils
    print("Connecting to network")
    networkUtils.connect_to_network(secrets.wifi_network, secrets.wifi_password, hostname=secrets.mqtt_device_id)

    print("Connecting to MQTT broker")
    client = MQTTClient(client_id=secrets.mqtt_device_id,
                        server=secrets.mqtt_server,
                        user=secrets.mqtt_user,
                        password=secrets.mqtt_password,
                        ssl=False)
    client.connect()

    print("Connected")

    return client


def main():
    pin = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    sensor = dht.DHT22(pin)

    mqttClient = connect()

    while True:
        try:
            sensor.measure()
            temperature = round((sensor.temperature() * 1.8) + 32, 2)
            humidity = sensor.humidity()

            reading = {
                "device": secrets.mqtt_device_id,
                "location": LOCATION,
                "temperature_F": temperature,
                "humidity": humidity
            }

            print(reading)

            mqttClient.publish(TOPIC, ujson.dumps(reading), qos=0)

            # Wait at least 2 seconds before next reading, since the DHT sensor can only
            # be read once every 2 seconds
            time.sleep(READING_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print('Bye')
            mqttClient.disconnect()
            break
        except OSError:
            mqttClient = connect()


# ------- Main program execution starts here --------
main()
