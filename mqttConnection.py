from simple import MQTTClient
import credentials.mqttCredentials as mqttCreds
import pinsInit as Pin
from pinsInit import DEVICE_ID, DEVICE_NAME, BOOTLE_750_ML_HEIGHT, BOOTLE_1500_ML_HEIGHT, SHAKER_HEIGHT
import json
import machine
import ubinascii
import gc
import os
from helpers.timeFormat import TimeFormat, getCurrentTime
from helpers.helpers import blink
from bh1750 import BH1750


class MQTTClientWrapper(MQTTClient):
    # Wrapper class with customized messages
    def on_mqtt_msg(self, topic, msg):
        # Callback function to handle received MQTT messages

        topic_str = topic.decode()
        msg_str = msg.decode()

        try:
            msg_json = json.loads(msg_str)
            destination_device_id = msg_json.get("device_id")
            operation = msg_json.get("operation")

            print(f"RX: {topic_str}\t{msg_str}")

            if destination_device_id == DEVICE_ID:
                if topic_str == mqttCreds.MQTT_ONBOARD_LED_TOPIC:
                    if operation == "on":
                        Pin.onboard_led.on()
                    elif operation == "off":
                        Pin.onboard_led.off()
                    elif operation == "toggle":
                        Pin.onboard_led.toggle()
                    self.mqtt_publish_pins_state()

                if topic_str == mqttCreds.MQTT_RELAY1_LED_TOPIC:
                    if operation == "on":
                        Pin.relay1_led.on()
                    elif operation == "off":
                        Pin.relay1_led.off()
                    elif operation == "toggle":
                        Pin.relay1_led.toggle()
                    self.mqtt_publish_pins_state()

                if topic_str == mqttCreds.MQTT_RELAY2_PUMP_TOPIC:
                    if operation == "on":
                        Pin.relay2_pump.on()
                    elif operation == "off":
                        Pin.relay2_pump.off()
                    elif operation == "toggle":
                        Pin.relay2_pump.toggle()
                    self.mqtt_publish_pins_state()

                if topic_str == mqttCreds.MQTT_PINS_STATE_TOPIC:
                    if operation == "check":
                        self.mqtt_publish_pins_state()

        except ValueError as e:
            print(f"JSON parsing error: {e}")

    def mqtt_publish_environment_data(self, timer, mqtt_client):
        topic_str = mqttCreds.MQTT_ENVIRONMENT_DATA_TOPIC

        slope = -0.00281
        intercept = 178.64

        soilHumidity = slope * Pin.soil_humidity.read_u16() + intercept

        VL53L0X_reading = 0.0
        for i in range(10):
            # Ranging loop for sensor
            VL53L0X_reading = Pin.VL53L0X.ping()-50

        waterRemaining = SHAKER_HEIGHT - VL53L0X_reading
        waterLevel = (waterRemaining / SHAKER_HEIGHT) * 100
        if waterLevel < 0:
            waterLevel = 0.0

        msg_json = json.dumps(
            {"device_id": DEVICE_ID,
             "device_name": DEVICE_NAME,
             "ambient_temperature": Pin.AHT10.temperature,
             "ambient_humidity": Pin.AHT10.relative_humidity,
             "soil_humidity": soilHumidity,
             "solar_irradiance": Pin.BH1750.luminance(BH1750.ONCE_LOWRES),
             "water_level": waterLevel,
             "timestamp": getCurrentTime(TimeFormat.SQL_FORMAT)})

        print(f"TX: {topic_str}\t{msg_json}")
        mqtt_client.publish(topic_str, msg_json)
        blink()

    def mqtt_publish_device_statistics(self, timer, mqtt_client):
        topic_str = mqttCreds.MQTT_DEVICE_STATISTICS_TOPIC

        ADC_voltage = Pin.onboard_temperature.read_u16() * (3.3 / (65535))
        board_temperature = 27 - (ADC_voltage - 0.706) / 0.001721

        s = os.statvfs('/')
        mem_alloc = gc.mem_alloc()
        mem_free = gc.mem_free()
        total_mem = mem_alloc + mem_free
        percent_used = (mem_alloc / total_mem) * 100

        msg_json = json.dumps(
            {"device_id": DEVICE_ID,
             "device_name": DEVICE_NAME,
             "board_temperature": board_temperature,
             "i2c_bus": [hex(int(num)) for num in Pin.i2c.scan()],
             "free_storage_KB": s[0]*s[3]/1024,
             "memory_used_percentage": percent_used,
             "cpu_freq_MHz": machine.freq()/1000000,
             "timestamp": getCurrentTime(TimeFormat.SQL_FORMAT)})

        print(f"TX: {topic_str}\t{msg_json}")
        mqtt_client.publish(topic_str, msg_json)
        blink()

    def mqtt_publish_pins_state(self):
        topic_str = mqttCreds.MQTT_PINS_STATE_TOPIC

        msg_json = json.dumps(
            {"device_id": DEVICE_ID,
             "device_name": DEVICE_NAME,
             "i2c_bus": [hex(int(num)) for num in Pin.i2c.scan()],
             "relay1_led": Pin.relay1_led.value(),
             "relay2_pump": Pin.relay2_pump.value(),
             "timestamp": getCurrentTime(TimeFormat.SQL_FORMAT)})

        print(f"TX: {topic_str}\t{msg_json}")
        self.publish(topic_str, msg_json)
        blink()

    def send_mqtt_ping(self, timer, mqtt_client):
        # Callback function to periodically send MQTT ping messages to the MQTT broker
        print("TX: ping")
        mqtt_client.ping()
