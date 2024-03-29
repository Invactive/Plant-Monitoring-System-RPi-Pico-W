# Plant Monitoring System

This Plant Monitoring System is designed to automate plant care through real-time monitoring environment, watering and irradiating. It utilized several AWS services:

- **AWS IoT Core**: Used for gathering data and interacting with actuators remotely through MQTT topics.
- **AWS Relational Database**: Used for storing data from sensors and board in Postgres relational database.
- **AWS Lambda**: Used for passing data from MQTT topics directly to database and integrating API calls with database and AWS IoT Core.
- **AWS API Gateway**: Used for interacting with actuators and getting data from database using HTTP requests.

Due to AWS management costs, account was closed and those functionalities currently does not work.

## System Architecture
[<img src="img/system_architecture.svg" width=60% height=60%>](img/system_architecture.svg)

## Project Features

- **Real-Time Plant Monitoring**: Track soil moisture, temperature, ambient humidity, and light levels remotely.
- **Watering and Light exposure**: A water pump and diode can be operated through commands sent to proper MQTT topics.
- **Integration with AWS services**: AWS services allow to pass data from MQTT topics to database, interact with the board and retrieve historical data from database.

## Hardware Components

- **Raspberry Pi Pico W**: Acts as the central processing unit, connected directly to AWS IoT Core for sending data and receiving commands.
- **Actuators**:
  - **1W Full Spectrum Power Diode**: Provides supplemental lighting to the plant. Connected to 12V step-up converter through relay.
  - **Water Pump**: Allows for watering. Also connected to 12V through relay.
- **Sensors**:
  - **AHT10**: Monitors air temperature and humidity.
  - **BH1750**: Measures light intensity.
  - **VL53L0X**: Gauges the water level in the tank using laser beam reflection.
  - **Analog Soil Moisture Sensor**: Checks the soil's moisture.
- **2-Channel Relay**: Controls the diode and water pump.
- **Universal PCB Board**: All components are soldered for a compact and robust system.

## Project Pictures

<p align="left">
  <img src="img/1706690138916.jpg" alt="1706690138916" height="500px"/>
  <img src="img/1706690139130.jpg" alt="1706690139130" height="500px"/>
</p>

## Remote Monitoring and Control through AWS IoT Core:
Remote connection and control could be executed through MQTT topics:

- **/environment-data**: Used for passing data from sensors.
- **/statistics**: Used for passing data about board (CPU and memory usage, board temperature, devices connected to I2C bus).
- **/pins-state**: Used for passing current data about used GPIOs.
- **/relay1-led**: Used for controlling 1st relay channel connected to power diode.
- **/relay2-pump**: Used for controlling 2st relay channel connected to water pump.
    - Example JSON payload to control relay (has to be published on /relay1-led or /relay2-pump topic):
      ```json
      // device_id is an id of RPi board obtained from ubinascii.hexlify(machine.unique_id()).decode()
      // operation accepts commands "on", "off" or "toggle"
      {
        "device_id": "<device_id>",
        "operation": "toggle"
      }
      ```
      
---

Project based on Raspberry Pi Pico W. Code written in MicroPython.
