import serial
import json
import requests

# Configure the serial connection
ser = serial.Serial('COM9', 115200)  # Replace 'COM9' with the appropriate port

# Server URL or API endpoint
server_url = 'http://localhost:8000/api/fall-detection-data/'

while True:
    # Read a line from the serial output
    line = ser.readline().decode('utf-8').strip()
    
    try:
        # Parse the JSON string
        data = json.loads(line)
        print("Received JSON data:", data)
        
        # Check the predicted activity
        if data['predicted_activity'] == 'Fall':
            # Trigger the emergency module
            print("Fall detected! Initiating emergency response.")
            
            # Prepare the fall detection data
            fall_data = {
                'sample_num': data['sample_num'],
                'predicted_activity': data['predicted_activity'],
                'accel_x': data['accel_x'],
                'accel_y': data['accel_y'],
                'accel_z': data['accel_z']
            }
            
            try:
                # Send the data to the server using HTTP POST request
                response = requests.post(server_url, json=fall_data)
                
                # Check the response status code
                if response.status_code == 201:
                    print("Data sent to the server successfully.")
                else:
                    print("Failed to send data to the server.")
                    print("Response status code:", response.status_code)
                    print("Response content:", response.content)
            except requests.exceptions.RequestException as e:
                print("Error occurred while sending data to the server:", e)
        
        else:
            print(f"Current activity: {data['predicted_activity']}")
    
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        print("Invalid JSON string received.")