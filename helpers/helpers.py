def check_file_in_folder(folder: str, file: str):
    import os

    if file in os.listdir(folder):
        print("The file exists.")
        return True
    else:
        print("The file does not exist.")
        return False


def install_package(source: str):
    import credentials.localNetworkCredentials as localNetCreds
    import network
    import time
    import mip

    wlan = network.WLAN(network.STA_IF)

    print(f"Connecting to Wi-Fi SSID: {localNetCreds.WIFI_SSID}")

    wlan.active(True)
    wlan.connect(localNetCreds.WIFI_SSID, localNetCreds.WIFI_PASSWORD)

    while not wlan.isconnected():
        time.sleep(0.5)

    print(f"Connected to Wi-Fi SSID: {localNetCreds.WIFI_SSID}")
    print(f"IP address: {wlan.ifconfig()}")

    mip.install(source)


# Read PEM file and return byte array of data
def read_pem(file: str):
    import ubinascii

    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])

        return ubinascii.a2b_base64(base64_text)


# Update the current time on the board using NTP
def updateCurrentTimeNTP():
    from .timeFormat import TimeFormat, getCurrentTime
    import time
    import ntptime

    while True:
        try:
            ntptime.settime()
            print(
                f"NTPtime set. Current time: {getCurrentTime(TimeFormat.SQL_FORMAT)}")
            break
        except Exception as e:
            print("npttime.settime() failed. Exception:", e)
            time.sleep(1)


# Toggle onboard led for debugging purposes
def blink():
    import pinsInit as Pin
    import time

    Pin.onboard_led.on()
    time.sleep(0.1)
    Pin.onboard_led.off()
