"""
    --------------------------------------------------------------------------------------
    networkUtils.py
    --------------------------------------------------------------------------------------

    Here are a few useful shortcut functions for working with networks.

    This file is imported by other examples that use networking.
    Replace the wifi name and password with your own network credentials, and ensure that
    this file is uploaded to your ESP8266 or ESP32 before running those scripts.

    Some examples of use:
        import networkUtils
        networkUtils.connect_to_network("mynetwork", "password")

        # Enable AP mode
        import networkUtils
        networkUtils.start_access_point("atomant", "up up and away!")
        ap = networkUtils.get_access_point()
        print(ap.ifconfig())

        # Connect to a wifi network in Station mode
        import networkUtils
        networkUtils.connect_to_network("network name", "password")
        station = networkUtils.getStation()
        print(station.ifconfig())
        print(station.isconnected())

    Author:  David Alexis (2019)
    --------------------------------------------------------------------------------------
"""


def get_access_point():
    import network
    return network.WLAN(network.AP_IF)


def get_station():
    import network
    return network.WLAN(network.STA_IF)


def start_access_point(ap_essid, ap_password):
    ap = get_access_point()
    currentEssid = ap.config('essid')

    if not ap.active():
        ap.active(True)

    if currentEssid != ap_essid:
        ap.config(essid=ap_essid, password=ap_password)
    else:
        ap.config(password=ap_password)

    print("Configured accesspoint %s" % (ap.config('essid')))


def connect_to_network(network_name, password, hostname=None, disableAP=True):
    import time

    if disableAP:
        ap = get_access_point()

        if ap.active():
            ap.active(False)

    station = get_station()

    # Determine if station mode is active.  If it is not, enable it and
    # connect to the network
    if not station.active():
        station.active(True)

    if hostname:
        station.config(dhcp_hostname=hostname)

    if not station.isconnected() or station.config('essid') != network_name:
        station.connect(network_name, password)

        while station.isconnected():
            print('Waiting for network connection...')
            time.sleep(0.5)
