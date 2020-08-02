"""
https://www.samkear.com/hardware/connecting-a-micro-sd-card-adapter-to-the-esp8266-development-board
"""

import machine
import os
import sdcard

sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))
os.mount(sd, '/sd')
os.listdir('/sd')
