def connectToWiFiNetwork(ssid: str, password: str):
    import network
    import time

    wlan = network.WLAN(network.STA_IF)

    print(f"Connecting to Wi-Fi SSID: {ssid}")

    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        time.sleep(0.5)

    print(f"Connected to Wi-Fi SSID: {ssid}")
    print(f"IP address: {wlan.ifconfig()}")
