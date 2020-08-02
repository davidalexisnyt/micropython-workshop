from machine import I2C, Pin
import time
import ssd1306
import framebuf

i2c = I2C(-1, Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

ICON = [
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 1, 0, 0, 0, 1, 1, 0],
     [1, 1, 1, 1, 0, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 1, 1, 1, 1, 1, 1, 1, 0],
     [0, 0, 1, 1, 1, 1, 1, 0, 0],
     [0, 0, 0, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0],
 ]

while True:
    display.fill(0)  # Clear the display
    for y, row in enumerate(ICON):
        for x, c in enumerate(row):
            display.pixel(x, y, c)

    display.text("Hello world!", 20, 3, 1)
    display.show()

    # FrameBuffer needs 2 bytes for every RGB565 pixel
    fbuf = framebuf.FrameBuffer(bytearray(10 * 100 * 2), 128, 32, framebuf.MONO_HLSB)
    time.sleep(5)

    display.fill(0)
    fbuf.fill(0)
    fbuf.text('MicroPython!', 0, 0, 0xffff)

    display.blit(fbuf, 10, 15)
    display.show()

    time.sleep(5)
