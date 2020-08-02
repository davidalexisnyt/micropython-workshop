"""
    --------------------------------------------------------------------------------------
    socketServer.py
    --------------------------------------------------------------------------------------
    Serves a web page from the ESP8266 that allows remotely turning a light on and off.

    This example was inspired by a great Random Nerd Tutorials post:
    https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

    Dependencies
    ------------
        - networkUtils.py
        - networkCredentials.py
        - index.html

    Parts
    ---------
        1 LED (whatever color you like)
        1 Resistor (4.7K to 10K)

    Wiring
    ---------
        ESP8266 GPIO5         -> LED +ve pin
        LED -ve pin           -> resistor
        Other end of resistor -> GND

    Note:   The print() statements in the code are there for debugging, and can only be
            seen when the program is run from the board's REPL.
            The statements should be removed or commented out if you don't want this
            debugging information.

    Author:  David Alexis (2019)
    --------------------------------------------------------------------------------------
"""

import socket
import machine
import os
import sys
import gc
import networkUtils
from machine import Pin
import secrets

led = Pin(16, Pin.OUT)
htmlTemplate = ''


def htmlPage():
    """
    Replaces the {LED_STATE} placeholder in our HTML template with the current
    on/off state of the LED.
    """
    if led.value() == 1:
        current_state = "on"
        next_state = "off"
    else:
        current_state = "off"
        next_state = "on"

    return htmlTemplate.replace("{LED_STATE}", current_state).replace("{NEXT_LED_STATE}", next_state)


# ------ Main script execution starts here ------

# Start the garbage collector
gc.collect()

networkUtils.connect_to_network(secrets.wifi_network, secrets.wifi_password, hostname="fireant")
print("My IP address is {}".format(networkUtils.get_station().ifconfig()[0]))

# Read our HTML template from storage.
# The HTML content contains placeholders {LED_STATE} and {NEXT_LED_STATE} that we
# will replace with the current LED state whenever it changes.
with open('index.html', 'r') as htmlFile:
    htmlTemplate = htmlFile.read()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)

# Main loop
# Listens for incomming socket requests, and toggles the LED as indicated
# in the request.
while True:
    try:
        print("Waiting")
        connection, address = sock.accept()
        print("Got connection from {}".format(address[0]))

        request = str(connection.recv(1024))

        if request.find('/?led=on') == 6:
            print('LED ON')
            led.on()
        elif request.find('/?led=off') == 6:
            print('LED OFF')
            led.off()

        response = htmlPage()

        connection.send('HTTP/1.1 200 OK\n')
        connection.send('Content-Type: text/html\n')
        connection.send('Connection: close\n\n')
        connection.sendall(response)
        connection.close()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
    except:
        pass
