import helpers.helpers as helpers
import credentials.localNetworkCredentials as localNetCreds
from networkConnection import connectToWiFiNetwork
from pinsInit import DEVICE_ID


print("Device ID:", DEVICE_ID)

connectToWiFiNetwork(localNetCreds.WIFI_SSID, localNetCreds.WIFI_PASSWORD)

if (not helpers.check_file_in_folder("lib", "simple.py")):
    helpers.install_package(
        "https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.simple/umqtt/simple.py")
else:
    print("MQTT package already installed")

if (not helpers.check_file_in_folder("lib", "ahtx0.py")):
    helpers.install_package(
        "https://raw.githubusercontent.com/targetblank/micropython_ahtx0/master/ahtx0.py")
else:
    print("ATHX0 package already installed")

if (not helpers.check_file_in_folder("lib", "bh1750.py")):
    helpers.install_package(
        "https://raw.githubusercontent.com/alaub81/rpi_pico_scripts/main/lib/bh1750.py")
else:
    print("BH1750 package already installed")

if (not helpers.check_file_in_folder("lib", "vl53l0x.py")):
    helpers.install_package(
        "https://raw.githubusercontent.com/kevinmcaleer/vl53l0x/master/vl53l0x.py")
else:
    print("VL53L0X package already installed")
