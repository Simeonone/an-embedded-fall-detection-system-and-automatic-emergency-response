import asyncio
import json
from bleak import BleakClient, BleakScanner

FALL_DATA_CHARACTERISTIC_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
device_address = "9e:52:0a:80:60:c6"  # Your Arduino's address

def notification_handler(sender, data):
    try:
        decoded_data = json.loads(data.decode())
        print(f"Received data: {decoded_data}")
        # Here you can add logic to handle fall detection
        if decoded_data['predicted_activity'] == 'Fall':
            print("FALL DETECTED!")
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