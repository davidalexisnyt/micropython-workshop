"""
    The ESP32 build of MicroPython leaves debugging on by default, for some reason,
    and this leads to annoying debugging output in the REPL.
    Calling the esp.osdebug(None) function disables it.

    Having this code in boot.py ensures that it will automatically get run
    every time the device starts up.

    We're also going to call gc.collect() to start up the garbage collector.
"""

import esp
import gc

esp.osdebug(None)
gc.collect()
