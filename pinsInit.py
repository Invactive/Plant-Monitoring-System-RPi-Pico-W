import time
import machine
import ubinascii
import bh1750
import ahtx0
import vl53l0x


# Define device name
DEVICE_NAME = "Raspberry-Pi-Pico-W-JG"
DEVICE_ID = ubinascii.hexlify(machine.unique_id()).decode()

# Define height of bootle of water for watering in mm
BOOTLE_750_ML_HEIGHT = 235.0
BOOTLE_1500_ML_HEIGHT = 320.0
SHAKER_HEIGHT = 145.0

# Create objects for on-board pins
onboard_led = machine.Pin("LED", machine.Pin.OUT)
relay1_led = machine.Pin(22, machine.Pin.OUT)
relay2_pump = machine.Pin(28, machine.Pin.OUT)
onboard_temperature = machine.ADC(4)
soil_humidity = machine.ADC(machine.Pin(26))

# Define i2c interface for sensors.
i2c_scl = machine.Pin(17)
i2c_sda = machine.Pin(16)
i2c = machine.SoftI2C(scl=i2c_scl, sda=i2c_sda)

# AHT10 temperature & humidity sensor. Default dddress: 0x38
AHT10 = ahtx0.AHT10(i2c)

# BH1750 solar irradiance sensor. Default address: 0x23
BH1750 = bh1750.BH1750(i2c)

# VL53L0X proximity ToF sensor. Default address: 0x8A
VL53L0X = vl53l0x.VL53L0X(i2c)
VL53L0X.set_measurement_timing_budget(40000)

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
VL53L0X.set_Vcsel_pulse_period(VL53L0X.vcsel_period_type[0], 12)

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
VL53L0X.set_Vcsel_pulse_period(VL53L0X.vcsel_period_type[1], 8)
