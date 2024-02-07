# File with MQTT client and broker credentials
# Place certificates from AWS IoT Core in credentials/certificates directory
from helpers.helpers import read_pem
import ubinascii
import machine


DEVICE_ID = ubinascii.hexlify(machine.unique_id()).decode()

# MQTT client constants
MQTT_CLIENT_KEY = "/credentials/certificates/****-private.pem.key"
MQTT_CLIENT_CERT = "/credentials/certificates/****-certificate.pem.crt"
MQTT_CLIENT_ID = DEVICE_ID

# MQTT broker constants
MQTT_BROKER = "***.iot.eu-central-1.amazonaws.com"
MQTT_BROKER_CA = "/credentials/certificates/AmazonRootCA1.pem"

# Read the data in the private key, public certificate, and root CA files
key = read_pem(MQTT_CLIENT_KEY)
cert = read_pem(MQTT_CLIENT_CERT)
ca = read_pem(MQTT_BROKER_CA)

# MQTT topic constants
MQTT_ONBOARD_LED_TOPIC = "/onboard-led"
MQTT_ENVIRONMENT_DATA_TOPIC = "/environment-data"
MQTT_RELAY1_LED_TOPIC = "/relay1-led"
MQTT_RELAY2_PUMP_TOPIC = "/relay2-pump"
MQTT_DEVICE_STATISTICS_TOPIC = "/statistics"
MQTT_PINS_STATE_TOPIC = "/pins-state"
