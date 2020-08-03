"""
    --------------------------------------------------------------------------------------
    blinky2.py
    --------------------------------------------------------------------------------------

    Shows a slightly different way to access the Pin class, refactors the toggling of the
    LED into a reusable function, and performs

    Author:  David Alexis (2019)
    --------------------------------------------------------------------------------------
"""

# Here we import the Pin class from the machine module so that we don't have to refer
# to it with "machine.Pin". This saves typing, but is also much more efficient.
from machine import Pin
from time import sleep_ms


# Let's also refactor the code that turns the LED on and off into a function
# so we can reuse it.
def blink(led, duration):
    """
    Turn on the LED for the specified amount of time, then turn it off
    """
    led.on()
    sleep_ms(duration)
    led.off()
    sleep_ms(duration)


# ------- Main program execution starts here --------

led1 = Pin(2, Pin.OUT)

while True:
    blink(led1, 200)
    blink(led1, 200)
    blink(led1, 1000)
