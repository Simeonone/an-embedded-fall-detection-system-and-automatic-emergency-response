import asyncio
import json
import requests
from bleak import BleakClient, BleakScanner

FALL_DATA_CHARACTERISTIC_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
device_address = "9e:52:0a:80:60:c6"  # The Arduino's address
server_url = 'http://localhost:8000/api/fall-detection-data/'

def notification_handler(sender, data):
    try:
        decoded_data = json.loads(data.decode())
        print(f"Received data: {decoded_data}")
        
        # Check the predicted activity
        if decoded_data['predicted_activity'] == 'Fall':
            print("FALL DETECTED! Initiating emergency response.")
            
            # Prepare the fall detection data
            fall_data = {
                'sample_num': decoded_data['sample_num'],
                'predicted_activity': decoded_data['predicted_activity'],
                'accel_x': decoded_data['accel_x'],
                'accel_y': decoded_data['accel_y'],
                'accel_z': decoded_data['accel_z']
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
            print(f"Current activity: {decoded_data['predicted_activity']}")
    except json.JSONDecodeError:
        print(f"Received non-JSON data: {data}")

async def run(address):
    while True:
        try:
            device = await BleakScanner.find_device_by_address(address, timeout=20.0)
            if not device:
                print(f"Could not find device with address {address}")
                await asyncio.sleep(5)
                continue

            async with BleakClient(device) as client:
                print(f"Connected: {client.is_connected}")
                
                await client.start_notify(FALL_DATA_CHARACTERISTIC_UUID, notification_handler)
                
                print("Waiting for data... Press Ctrl+C to stop.")
                while True:
                    await asyncio.sleep(0.1)  # Smaller sleep interval for faster response

        except asyncio.CancelledError:
            # Handle graceful shutdown
            print("Shutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Attempting to reconnect in 5 seconds...")
            await asyncio.sleep(5)

async def main():
    try:
        await run(device_address)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")

if __name__ == "__main__":
    asyncio.run(main())