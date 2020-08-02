import network
import urequests
import secrets

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(secrets.wifi_network, secrets.wifi_password)

while not wifi.isconnected():
    pass

ip_address = wifi.ifconfig()[0]
print('Connected! IP address: {}'.format(ip_address))

response = urequests.get('https://httpbin.org/get')
print(response.text)
