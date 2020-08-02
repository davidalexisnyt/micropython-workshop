"""
    --------------------------------------------------------------------------------------
    mqttSubscriber.py
    --------------------------------------------------------------------------------------
    Demonstrates how to subscribe to an MQTT topic. It listens to the sensors topic to
    which the dht_sensor_mqtt.py program publishes.

    Author:  David Alexis (2020)
    --------------------------------------------------------------------------------------
"""

import time
import machine
import ubinascii
from umqtt.robust import MQTTClient
import secrets


# We're using a wildcard in the topic path so that we receive any message sent to any
# sub-topic under 'sensors'.
topic = 'sensors/#'

# ESP8266 and ESP32 chips contain a built-in unique ID.  The machine.unique_id()
# function returns a unique identifer as a byte array.  We must first convert it
# to a hex string to make it human-readable.
client_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
print("My client ID is {}".format(client_id))


def subscription_handler(topic, msg):
    print(topic.decode('utf-8'), " :: ", msg.decode('utf-8'))


def connect():
    import networkUtils
    print("Connecting to network")
    networkUtils.connect_to_network(secrets.wifi_network, secrets.wifi_password)

    print("Connecting to MQTT broker")
    client = MQTTClient(client_id=client_id,
                        server=secrets.mqtt_server,
                        user=secrets.mqtt_user,
                        password=secrets.mqtt_password,
                        ssl=False)
    client.set_callback(subscription_handler)
    client.connect()
    client.subscribe(topic)

    print("Connected")

    return client


# ------ Main script execution starts here ------

client = connect()

while True:
    try:
        client.check_msg()
        time.sleep(.1)
    except OSError:
        client = connect()
