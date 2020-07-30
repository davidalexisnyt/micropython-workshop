<h1 style="font-weight: bold; font-size: 250%">Python in Small Places: Intro to MicroPython</h1>



# Introduction to MicroPython

Developing for microcontrollers was previously the domain of electrical engineers who used assembler and/or C/C++ with complicated toolchains and lengthy build processes. This changed radically with the introduction of Adruino, which radically simplified the coding and build process, and the provided a platform that made DIY electronics and prototyping accessible to a much wider audience. But you still had to learn to program in C/C++, which, while not terribly difficult, still presented a barrier for entry.

Python is one of the most popular languages, for good reason. It is clean and powerful, allowing developers to be very productive. Programmers get immediate feedback to their changes without having to wait for the code to compile and deploy. Need to quickly check if something would work as expected? Jump into the REPL, execute a few commands, and see their results immediately. What if you can have the power and simplicity of the Arduino platform, but with the rapid feedback loop and productivity of Python?

This is what MicroPython provides. In this course, we're going to learn about MicroPython, how to install it on Internet of Things (IoT) devices, see various development environment options, and build a working IoT application that transmits sensor readings over WiFi.

Let's get started!



# Know Your Board

There are two types of microcontroller boards that we'll talk about.

## ESP8266-based boards

The ESP8266 is the chip that arguably started the do-it-yourself (DIY) IoT revolution, and was created by Espressif, a company based in Shanghai, China.  It contains a 32-bit processor running at 80MHz, with 64K of RAM and 4MB flash storage.  That's 5 times the processing power, 16 times the RAM, and 128 times the storage of a typical Arduino board.  But the killer feature is a built-in WiFi stack that can act as a WiFi client, access point, or both at the same time!  These boards can be obtained for as little as $4 in the US and under $1 from China. The ESP8266 was initially marketed as an add-on WiFi component for other microcontrollers, like Arduino.  Then someone realized that it contained its own

<img src="part1-images/image-20200727195603905.png" alt="image-20200727195603905" style="zoom:50%;" />





## ESP32-based boards

Following on the success of the ESP8266, Espressif came up with the ESP32.  This has a dual-core 32-bit processor running at between 160MHz and 240MHz, faster WiFi, Bluetooth, and lots more I/O ports.  In addition to the standard "developer board" form factors, this chip comes in interesting packages like the ESP Cam (a 2MP camera for video streaming and still imaging for about $8) and the ESP-AI (camera plus built-in face-detecting AI in hardware).

<img src="part1-images/developing-for-espressif-esp32-and-esp8266.png" alt="Develop for espressif esp32 and esp8266 by Carstent" style="zoom: 50%;" />





## Pinouts

One important term you will come across often is "pinout".  A pinout is a visual map of a board or component.  Having a pinout diagram of your board (and/or whatever component you're trying to work with) handy saves lots of time and frustration.  When you're trying to hook up your temperature sensor, for instance, it's very important to know which pin connects to the power and which connects to ground, otherwise it won't work (at best) or there will be fireworks (at worst).  

These diagrams are readily available on the Internet, and can be obtained by searching for "pinout" plus whatever board or component you're interested in.  For example, the following diagram of a typical ESP8266 development board can be found by Googling, `esp8266 pinout`.  If you have an ESP32 board, search for `esp32 pinout`.

![Understanding NodeMCU ESP8266-12E Limitations - Making It Up](images/NodeMCU-ESP8266-12E-Limitations.jpg)

There are a few things to take note of on this diagram:

- The pin labels printed on the board itself are different from the callout labels that say, "GPIO<number>".  If you're working with the Arduino development environment, there are sometimes constants defined for given boards, where you can reference pins in your code as `D5` or `A1`.  The "GPIO" (General Purpose Input/Output) pin numbers are the actual pin numbers of the underlying microcontroller chip, and in the case of ESP8266 and ESP32 boards, the pins are not labeled to match the GPIO pin numbers.  `¯\_(ツ)_/¯`.
- In MicroPython, the GPIO labels are the ones you need to take note of and reference in your code.
- There are a number of different color coded labels for some pins.  Those pins serve special purposes, sometimes multiple purposes.  For example, the green labels represent the connections to use for SPI (serial peripheral interface) components.  The orange labels are for I2C (inter-integrated circuit) connections.  The blue labels are for basic transmit/receive connections.  The purple label shows the single analog/digital I/O pin on the ESP8266.  The ESP32 has 18 such pins for analog I/O, as well as a few pins for digital to analog conversions.

Find the pinout diagram for your particular board, and keep it handy.  Note:  AdaFruit's boards have a very different layout, but it seems that many board makers are catching on to their layout design.

The ESP boards work on 3.3 volts. This is important for two main reasons.  The board will get damaged if you feed it any more than 3.3V on any of the pins labeled `3.3V`.  Batteries or other power supplies ranging from 5V to 12V can be supplied to the `Vin` (voltage in) pin, although it is not advised to go over 9 volts. (I once connected a 9 volt supply to Vin on a cheap ESP8266, and it exploded.) The other importance of the 3.3 volts is that these boards will only work with components designed for up to3.3V.  Make sure that any components you try to use are not 5V-rated.  Some components, like the DHT sensor we will use, work with anything from 2 to 5 volts, so they work perfectly with ESP boards.



# Working With a Breadboard



![image-20200728143040376](images/image-20200728143040376.png)

One of the most important tools in the electronics prototyping toolbox is the breadboard. It is used to build circuits and connect components in a non-permanent way. Once you’ve built and tested the circuit, you can then move on to soldering it in a more permanent, and more compact, way on perfboard or a specially designed printed circuit board (PCB).

A breadboard is like a pin cushion for connecting things, with a grid of holes that are connected electrically. There are two parts to a breadboard - the main area consisting of groups of **terminal strips** where components are inserted and arranged, and the **power rails** along the top and bottom.

Here we see how a breadboard is connected internally.

![img](images/breadboard_internal.png)

The main area consists of a two separate grids of holes arranged in usually 30 or more columns (labeled 1 through 30) of 5 holes (labeled a through e, and f through j), separated by a groove. Each column of 5 holes is called a terminal strip. All of the 5 holes (or **tie points**) in a column are connected together internally.

The power rails are along the top and bottom of the breadboard, and each consists of two strips of tie points. The power strip (+ve voltage) is marked with a **+** and a red line. The ground rail is marked with a **-** and a line that is either black or blue.

Power and ground are typically fed to the breadboard from the 5V (or 3.3V) and GND pins on the Arduino, and the strips are then used to feed power and ground to components of your circuit. We’ll see this in action later.



# Tool and Development Environment Setup

Set up Python virtual environment to host the basic tools.

Create a folder somewhere to hold our virtual environment and MicroPython projects.  For example, I have my code set up under C:\code\iot on my Windows machine and ~/code/iot on my Linux environment.  Create your own based on your preference, but for this document, let's assume ~/code/iot.

First, let's go to that folder and create a new virtual environment.

```shell
cd ~/code/iot
python3 -m venv iotenv
```

These commands will work just as shown in Powershell for Windows, except you would call Python with `python` or `py` instead of `python3`.

Let's activate the virtual environment.

```shell
source iotenv/bin/activate
```

In Windows Powershell:

```shell
./iotenv/scripts/activate.ps1
```

Now we will install a few tools that we'll use.  Esptool is used to flash MicroPython onto our board.

```shell
pip install esptool
esptool.py --version
```

Note that once installed, esptool must be called with the .py extension:  `esptool.py`.  Run it with no arguments to get help on its various commands.

Now let's install a few other tools that we'll walk through in more detail later.

```shell
pip install rshell
pip install adafruit-ampy
pip install mpfshell
```

- **rshell:**  Remote Shell for Micropython.  This lets you connect to your board, then presents what looks like a basic Linux-type shell that lets you copy files to and from the board, and the ability to launch a Python REPL on the board.
- **AdaFruit ampy:**  AdaFruit's MicroPython Tool.  This is a CLI tool - ampy - for copying files to and from your board, and to have very basic control over the board.  Ampy has fallen behind somewhat, and was even going to be discontinued by AdaFruit, but it lives on.
- **mpfshell:** MicroPython File Shell.  This is very similar to rshell, but does not use the somewhat confusing fake Linux user interface paradigm.  One cool advantage it has is the ability to pre-compile your code to byte code, which will save time and memory when the code executes on the device.

You don't need all three of these tools, but it's good to explore them all so you can see which one fits your preferences.



## IDE Choices

Since you don't have to worry about a compiler toolchain, you basically can choose any development environment that you like.  The differences between them come down to the the workflow of getting your Python files onto your board.  I have explored a number of options to try to provide information that is as objective as possible.

### Thonny

[Thonny](https://thonny.org/) is a simple Python IDE designed for beginners on devices like Raspberry Pi, and for working with MicroPython devices.  It doesn't have all the bells and whistles as a typical IDE, but where it shines is that it has the best integration with MicroPython devices.  Thonny works on Mac, Windows, and Linux.

### Visual Studio Code

VS Code is my IDE of choice, partly because of its extensibility through open source extensions.  Sadly, the MicroPython prospects range from barely OK to really bad.  So while VS Code would be great at editing your MicroPython code, you'll need to use other tools, like rshell, in conjunction.

### Atom

There is a plugin called Pymakr for both VS Code and Atom.  But while the VS Code version seems barely even workable, the Atom version works surprisingly well. It provides a UI within Atom that let's you connect to one or more boards, use the Python REPL on the board, run a particular Python file, reboot your board, and sync your "project" with the board.  The sync option copies the entire folder tree open in Atom to the board!  This burned me the first time, until I figured out how to select which folder gets synced and how to exclude files.  Atom + Pymakr is not perfect, but it's very workable.

### PyCharm

Lots of Python developers use PyCharm.  And it has a MicroPython plugin that supposedly works really well.  I couldn't get it to work.  This is not necessarily anything to do with PyCharm or the plugin, but more to do with my brain just not being in sync with most things from Jetbrains.

### vi, etc.

I'm not a vi person, but I would wager that someone out there, from deep within their mother's basement, has created the perfect vi plugin for MicroPython.

### Your Editor of Choice + Command Line Tools

I find myself using this option mostly.  I would play around with code snippets in Thonny, since it works so seamlessly with the board.  But once I'm ready to work the code into a piece of art, I'll switch to VS Code or Atom and use rshell or mpfshell to shuttle code to and from the device from the command line.



# MicroPython Installation

If you've worked with Arduino development, you know the compile/upload/run cycle well.  Your project code must first be compiled to a binary machine code targeted for a particular board.  The binary must then be flashed onto the board, and the board is reset.  Only then will you see whether the code worked. There's usually a lot of waiting around, which it typical when working with C/C++.

MicroPython is very different.  The MicroPython environment (compiler/interpreter) is the only thing that needs to get flashed to your board, and this is done only once.  From then on, you run code on the board simply by uploading changed .py files to the board and running them.  Need to see how a particular snippet of code behaves?  Launch the Python REPL on the board, and just start typing Python!  Too much to type? Put the REPL into paste mode, paste your code, and it runs. This is an exciting level of productivity for the microcontroller world.

Let's get Python onto that board!  The full details about the installation can be read on the [Quick Referfence](http://docs.micropython.org/en/latest/index.html) page for your particular board on the MicroPython site.

First, we need to download the latest stable build of MicroPython for our board.  Go to the [download page](http://micropython.org/download/) and click on the link for your board.  If you have an ESP8266 board, click the [Generic ESP8266 board](http://micropython.org/download/esp8266) link.  If you have an ESP32 board, click on the [Generic ESP32 board](http://micropython.org/download/esp32) link.  Download the latest stable build.  As of this writing, that was [esp8266-20191220-v1.12.bin](http://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin) for ESP8266 and [esp32-idf3-20191220-v1.12.bin](http://micropython.org/resources/firmware/esp32-idf3-20191220-v1.12.bin) for ESP32.  Once downloaded, copy/move the file to the `~/code/iot` folder (or whatever folder you created in the "Tool and Development Environment Setup" section above).

Now, connect your board and determine what port it is connected to.  On Windows, this will be a COM port, and on Mac and Linux, it will appear as a folder under the `/dev` folder.  We can use the rshell tool we previously installed to get this information:

```shell
rshell --list
```

You might see something like the following

on Mac:

```
USB Serial Device 10c4:ea60 with vendor 'Silicon Labs' serial '0001' found @/dev/cu.SLAB_USBtoUART
```

or on Windows:

```
USB Serial Device 10c4:ea60 with vendor 'Silicon Labs' serial '0001' found @COM9
```

or on Linux:

```
USB Serial Device 10c4:ea60 with vendor 'Silicon Labs' serial '0001' found @/dev/ttyUSB0
```

What you want to look for is the entry with "vendor 'Silicon Labs'". Take note of the port after the "@".

First, we need to erase anything that is currently on the board.  You will also need to do this if you ever want to re-install MicroPython onto a board (e.g. installing a new version).  This is done using esptool:

```shell
esptool.py --port <port> erase_flash
```

Replace `<port>` with the actual port your device is connected to.  For example, let's say we're on Linux and the board is connected to `/dev/ttyUSB0`.  The command would be:

```shell
esptool.py --port /dev/ttyUSB0 erase_flash
```



Once the command completes, the board will have nothing on it, and we can go ahead and install (flash) the actual MicroPython binary onto it.  There is no operating system involved.  The Python environment will be running on the "bare metal" of the board and acting as interpreter, compiler, and operating system.  The command to install it may be different for each type of board, and if definitely different for the ESP8266 and ESP32.  Be sure to use the right one.



To flash MicroPython to an **ESP8266** device:

```shell
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp32-idf3-20191220-v1.12.bin
```



To flash MicroPython to an **ESP32** device:

```shell
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20180511-v1.12.bin
```





> ESP32:  Change boot.py to do the following:
>
> ```python
> import esp
> esp.osdebug(None)
> ```
>
>





## REPL



Crtl-E - Paste mode

Ctrl-C - Stop currently running code

Ctrl-D - Soft reset





```python
from machine import Pin
import time


led1 = Pin(2, Pin.OUT)
led2 = Pin(16, Pin.OUT)

while True:
    led1.on()
    led2.off()
    time.sleep(1)
    led1.off()
    led2.on()
    time.sleep(1)
```







# The Sensor



![DHT11-DHT22-AM2302-Temperature-Humidity-Sensor-Pinout](images/DHT11-DHT22-AM2302-Temperature-Humidity-Sensor-Pinout.png)



<img src="part1-images/dht22_esp8266_wiring.png" alt="Getting Started With the ESP8266 and DHT22 Sensor" style="zoom: 50%;" />







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





Arduino Cloud:

Client ID:  8YOnoKPjeuO8KtBsqI8UQXkeDe6uGPGv

Client Secret:  H0Ax11m1EX7ArnAXK6RKc6dtsbAISf3rHJjnZd7cnU8du9TfnX4Ah2tFqPIQaU4o



| Current Endpoints |                                                              |
| ----------------- | ------------------------------------------------------------ |
| Web               | `https://io.adafruit.com/dalexis/feeds/makerweek-sensors`    |
| API               | `https://io.adafruit.com/api/v2/dalexis/feeds/makerweek-sensors` |
| MQTT *by Key*     | `dalexis/feeds/makerweek-sensors`                            |

```
IO_USERNAME  "dalexis"
#define IO_KEY       "52221012e80fa76a22af1ec0215b2103337caab9"
```

https://console.firebase.google.com/





## Attribution

Diagrams made with [Cirtuits.io](https://www.circuito.io/app)
