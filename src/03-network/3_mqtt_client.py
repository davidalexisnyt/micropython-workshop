import network
from umqtt.robust import MQTTClient
import secrets

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(secrets.wifi_network, secrets.wifi_password)

while not wifi.isconnected():
    pass

# Define some identifying information for our sensor node
DEVICE_ID = 'sensor1'

# Connect to the MQTT broker
print("Connecting to Mqtt...")
mqtt_client = MQTTClient(client_id=DEVICE_ID,
                         server=secrets.mqtt_server,
                         user=secrets.mqtt_user,
                         password=secrets.mqtt_password,
                         ssl=False)
mqtt_client.connect()

mqtt_client.publish('sensors/hello', 'Hello MQTT!')
