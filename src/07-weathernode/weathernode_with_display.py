import freesans20
import writer
from machine import I2C, Pin
import ssd1306
import framebuf
import dht
import utime
import gc


gc.collect()

dhtPin = Pin(2, Pin.IN, Pin.PULL_UP)
sensor = dht.DHT11(dhtPin)

i2c = I2C(-1, Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
font_writer = writer.Writer(display, freesans20, False)

icons = dict()


def displayIcon(iconname, top, left):
    
    icon = icons.get(iconname)
    blit = display.blit
    fb = framebuf.FrameBuffer
    
    if not icon:
        with open(iconname, 'rb') as f:
            _ = f.readline() # Magic number
            dim = f.readline().decode().strip()
            
            if dim.startswith('#'):
                dim = f.readline().decode().strip()
            
            w, h = [int(s) for s in dim.split(' ')] # Dimensions
            data = bytearray(f.read())
            icon = fb(data, w, h, framebuf.MONO_HLSB)
            icons[iconname] = icon
            
    blit(icon, top, left)


def show(tempC, tempF, hum):
    slen = font_writer.stringlen
    setp = font_writer.set_textpos
    prints = font_writer.printstring
    
    start = 30
    setp(start, 10)
    t = str(tempF)
    prints(t)

    start = start + slen(t) + 2
    displayIcon('fahrenheit.pbm', start, 10)
    start = start + 20
    setp(start, 10)
    t = str(tempC)
    print(t)
    prints(t)
    start = start + slen(t) + 2
    displayIcon('celcius.pbm', start, 10)

    start = 30
    setp(start, 40)
    t = str(hum)
    prints(t)
    start = start + slen(t) + 2
    displayIcon('percent.pbm', start, 40)
    display.show()


def run():
    # Show icons
    displayIcon('temperature.pbm', 10, 12)
    displayIcon('humidity.pbm', 10, 42)
    measure = sensor.measure
    temp = sensor.temperature
    hum = sensor.humidity
    sleep = utime.sleep
    
    while True:
        try:
            measure()
            tC = temp()
            tF = round((tC * 1.8) + 32)
            tC = round(tC)
            h = round(hum())
            show(tC, tF, h)
        except Exception as e:
            print('bad reading')
            print(e)

        sleep(5)

run()

