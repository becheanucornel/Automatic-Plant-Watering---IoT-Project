import paho.mqtt.client as mqtt
import time
import threading
import serial

# MQTT Variables
BROKER = "localhost"
PORT = 1883
TOPIC_SensorData = "sensordata"
TOPIC_PumpControl = "pumpcontrol"

# Global Variables
receive_control = False
humidity = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_PumpControl)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global receive_control
    receive_control = msg.payload.decode('utf-8').lower() == "true"
    print(f"Received from MQTT Topic '{msg.topic}': {receive_control}")

def mqtt_manager():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    while True:
        data = process_data()
        client.publish(TOPIC_SensorData, str(data))
        print(f"Published to MQTT Topic '{TOPIC_SensorData}': {data}")
        time.sleep(1)

def receive_sensordata():
    global humidity
    return {"humidity": humidity}

def process_data():
    sensor_data = receive_sensordata()
    current_humid = sensor_data.get("humidity", "N/A")
    return current_humid

def serial_com_arduino():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    global humidity
    while True:
        if ser.in_waiting > 0:
            humidity = ser.readline().decode('utf-8').strip()
            print(f"Humidity received from Arduino: {humidity}")

            # Send control command to Arduino
            string_rc = "true\n" if receive_control else "false\n"
            ser.write(string_rc.encode())
            print(f"Sent to Arduino: {string_rc.strip()}")
            time.sleep(1)

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=mqtt_manager, daemon=True)
    serial_thread = threading.Thread(target=serial_com_arduino, daemon=True)

    mqtt_thread.start()
    serial_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program...")
