"""
    MRFC522 library from https://github.com/wendlers/micropython-mfrc522
    Sample code modified to fix issues.
    
    --------------------------------------
                 MFRC522
                 Reader/PCD
     Signal      Pin          ESP8266 Pin
    --------------------------------------
     RST/Reset   RST          D1 (GPIO5)
     SPI SS      SDA(SS)      D2 (GPIO4)
     SPI MOSI    MOSI         D7 (GPIO13)
     SPI MISO    MISO         D6 (GPIO12)
     SPI SCK     SCK          D5 (GPIO14)
     3.3V        3.3V         3.3V
     GND         GND          GND

"""

import lib.mfrc522
from os import uname


def run():
    reader = mfrc522.MFRC522(sck=14, mosi=13, miso=12, rst=5, cs=4)

    print("--------------------------")
    print("Ready to read an RFID tag")
    print("--------------------------")

    while True:
        try:
            stat, tag_type = reader.request(reader.REQIDL)

            if stat == reader.OK:
                stat, raw_uid = reader.anticoll()

                if stat == reader.OK:
                    print("New card detected")
                    print("  - tag type: 0x{02x}".format(tag_type)
                    print("  - uid   : 0x{02x}{02x}{02x}{02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if reader.select_tag(raw_uid) == reader.OK:
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if reader.auth(reader.AUTHENT1A, 8, key, raw_uid) == reader.OK:
                            print("Data: {}".format(reader.read(8))
                            reader.stop_crypto1()
                        else:
                            print("Could not read tag data")
                    else:
                        print("Failed to select tag")

        except KeyboardInterrupt:
            print("Bye")
            break


run()
