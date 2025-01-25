# Automatic plant watering - IoT Project

This is one of our term projects for Embeded Systems.
For this project we used:
- Raspberry Pi 4
- Arduino MEGA 2560
- 5VDC Relay
- Submersive Water Pump
- Analog Humidity Sensor

We use the Arduino board as a slave board for collecting data from the sensors
and for controlling the relay which turn on/off the water pump.

We used Node-RED to create a dashboard interface, where we display
the humidity level of the plant's soil. Also we implemented a control system inside 
Node-RED which allows manual control and automatic control of the water pump.

This project uses two communication protocols:
- MQTT: Between the python script and Node-RED.
- Serial Communication: Between the Raspberry Pi and the Arduino board

## Python Script

The python script is the master of the entire system. We have multiple functions 
implemented into it which we run into two different threads, for better performance.
The first thread handles MQTT communication between the python script and Node-RED, 
sending and receiving data which is parsed to the Arduino board.
The second thread handles the Serial communication between the python script and 
the Arduino board, sending and receiving data from the sensors and controlling the water
pump.

## Arduino C Script

The C script running on the Arduino board is a slave script which sends data from the 
humidity sensor to the python script on the Raspberry Pi and also turn on the relay which
turn the water pump on when a command is received from the Raspberry Pi.

## Node-RED

The Node-RED is running locally on the Raspberry Pi and handles the control of the system.
Aside from the dashboard it has two control functions:
- Manual Control: On the dashboard there are two buttons for turning on and off the water pump.
- Automatic Control: We implemented a Control Flow which checks the humidity sensor data and
based on this turns on or off the water pump to ensure the constant humidity of the plant's soil.

## Demo 

There is a demo video inside the demo folder, where you can see how the entire project operates.

