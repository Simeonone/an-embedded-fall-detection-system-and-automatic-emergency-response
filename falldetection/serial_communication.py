import serial
import json
import requests
import time

# Establish a serial connection with the Arduino board
ser = serial.Serial('COM9', 115200)  # Replace 'COM3' with the appropriate serial port

# URL of your Django backend's API endpoint
url = 'http://localhost:8000/api/fall-detection-data/'
headers = {'Content-type': 'application/json'}

while True:
    print("Waiting for data...")
    if ser.in_waiting > 0:
        print("Data available")
        line = ser.readline().decode('utf-8').strip()
        print(f"Received data: {line}")
        
        try:
            data = json.loads(line)
            print("JSON data:")
            print(json.dumps(data, indent=2))
            
            # Send the data to your Django backend
            response = requests.post(url, data=json.dumps(data), headers=headers)
            print(f"Status code: {response.status_code}")
            
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
