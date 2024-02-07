import credentials.localNetworkCredentials as localNetCreds
import credentials.mqttCredentials as mqttCreds
from helpers.helpers import updateCurrentTimeNTP
import mqttConnection as mqtt
import machine
import ssl


updateCurrentTimeNTP()

print(f"Connecting to MQTT broker: {mqttCreds.MQTT_BROKER}")

mqtt_client = mqtt.MQTTClientWrapper(
    mqttCreds.MQTT_CLIENT_ID,
    mqttCreds.MQTT_BROKER,
    keepalive=60,
    ssl=True,
    ssl_params={
        "key": mqttCreds.key,
        "cert": mqttCreds.cert,
        "server_hostname": mqttCreds.MQTT_BROKER,
        "cert_reqs": ssl.CERT_REQUIRED,
        "cadata": mqttCreds.ca,
    },
)

# Register callback to for MQTT messages, connect to broker and subscribe topics
mqtt_client.set_callback(mqtt_client.on_mqtt_msg)
mqtt_client.connect()
mqtt_client.subscribe(mqttCreds.MQTT_ONBOARD_LED_TOPIC)
mqtt_client.subscribe(mqttCreds.MQTT_RELAY1_LED_TOPIC)
mqtt_client.subscribe(mqttCreds.MQTT_RELAY2_PUMP_TOPIC)
mqtt_client.subscribe(mqttCreds.MQTT_PINS_STATE_TOPIC)
# mqtt_client.subscribe(mqttCreds.MQTT_DATA_TOPIC)
# mqtt_client.subscribe(mqttCreds.MQTT_DEVICE_STATISTICS_TOPIC)

print(f"Connected to MQTT broker: {mqttCreds.MQTT_BROKER}")

# Create timer for periodic MQTT ping messages for keep-alive
mqtt_ping_timer = machine.Timer(
    mode=machine.Timer.PERIODIC,
    period=mqtt_client.keepalive * 1000,
    callback=lambda t: mqtt_client.send_mqtt_ping(t, mqtt_client)
)

# Create timer for periodic MQTT messages with temperature
mqtt_temperature_timer = machine.Timer(
    mode=machine.Timer.PERIODIC,
    period=30000,
    callback=lambda t: mqtt_client.mqtt_publish_environment_data(
        t, mqtt_client)
)

# Create timer for periodic MQTT messages with device statistics
mqtt_temperature_timer = machine.Timer(
    mode=machine.Timer.PERIODIC,
    period=120000//2,
    callback=lambda t: mqtt_client.mqtt_publish_device_statistics(
        t, mqtt_client)
)

# Main loop, continuously check for incoming MQTT messages
while True:
    mqtt_client.check_msg()
