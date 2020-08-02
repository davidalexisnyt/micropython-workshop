"""
    --------------------------------------------------------------------------------------
    dhtSensorOptimized.py
    --------------------------------------------------------------------------------------

    This script shows hot to use the DHT11/22 digital humidity and temperature sensors.

    This version of the script demonstrates some MicroPython optimization tips that make
    your code execute faster and use less memory.

    Note:  Although the optimization tips in this code are documented in long comments,
           this, in itself, goes against another MicroPython optimization tip - use
           as little comments as possible, since comments consume valuable storage space
           and make compilation slower (since the compiler needs to parse through it all).
           Remove all but essential comments in "production" code, and document your code
           extermally.

    Author:  David Alexis (2020)
    --------------------------------------------------------------------------------------
"""

import machine
from machine import Pin
import dht
import utime

import gc

# Start the garbage collector
gc.collect()

def main():
    """
        Optimization Tip: Wrap main code in a function.

        Code written in the global scope executes slower, since the Python interpreter
        needs to look up all symbols as dictionary lookups from the global symbol table.
        Global lookups in Python are expensive.  Wrapping the main functionality in a
        function moves symbol lookups (for variables, etc) to the local scope, which
        executes much faster in the Python interpreter.
    """

    """
    Optimization tip: Cache functions in local variables to prevent symbol table
    lookups.  e.g. accessing 'machine.Pin' must first do an expensive global lookup
    of 'machine', then do another dictionary lookup in 'machine' to get the contained
    'Pin' object. Caching 'machine.Pin' in the local 'pin' variable leads to calls to
    the referenced Pin to be up to 10 times faster than using 'machine.Pin()'.

    Here, we are caching all of the functions we'll be calling within the main
    execution loop.
    """
    pin = Pin(5, Pin.IN, Pin.PULL_UP)
    sensor = dht.DHT22(pin)
    measure = sensor.measure
    getTemp = sensor.temperature
    getHum = sensor.humidity
    sleep = utime.sleep

    while True:
        try:
            # Get sensor readings
            """
            Optimization tip: Using short variable names uses less memory.
            This is counter-intuitive, since longer, descriptive names make code more
            readable and maintainable. However, things are different in resource-constrained
            devices with very little memory. Python stores the full variable names in memory,
            and this obviously consumes a very limited resource.  Using shorter names helps
            reduce memory consumption, especially in larger programs.
            """
            measure()
            t = getTemp()
            h = getHum()

            if isinstance(t, float) and isinstance(h, float):
                tf = str(round(t * 1.8 + 32, 2))

                r = {
                    "temperature": tf,
                    "humidity": h
                }

                print(r)
            else:
                print("Could not get reading")
        except OSError:
            print("Sensor failed")

        # Wait at least 2 seconds before next reading, since the DHT sensor can only
        # be read once every 2 seconds
        sleep(2)

# ----- Program starts here
main()
