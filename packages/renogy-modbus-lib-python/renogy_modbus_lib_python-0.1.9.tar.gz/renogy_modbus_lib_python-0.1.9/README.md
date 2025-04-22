# RenogyBT for Python SDK

RenogyBT is a Python SDK designed for Modbus communication with Renogy products. This project provides functionality to communicate with Renogy devices via Bluetooth.

## Installation

Ensure your Python version is 3.6 or above. You can install the required dependencies using the following command:

```bash
pip install renogy-modbus-lib-python
```
## Usage
### Initialization
First, initialize the EnhancedModbusClient class to scan and connect to devices:

```python
from modbus_bt_pkg.src.renogy_lib_python import EnhancedModbusClient

async def main():
    client = EnhancedModbusClient(slave_address=0xFF)
    devices = await client.scan_devices()
    # Select and connect to a device
    success = await client.connect(selected_device['address'])
 ```

### Data Retrieval
Once connected, you can use the following methods to retrieve battery raw data and status information:

```python
response = await client.get_hole_original_data()

status = await client.get_status()
 ```
## Example
``` python
import asyncio
import sys
import os

from renogy_lib_python.modbus_comm import EnhancedModbusClient
async def main():
    client = EnhancedModbusClient(slave_address=0xFF) 
    connected = False
    choices = ["battery","controller"]
    try:
        # start scanning for devices
        devices = await client.scan_devices()  
        if len(devices):
            print("\nList of available devices:")
        for i, dev in enumerate(devices, 1):
            print(f"{i}. {dev['name']} ({dev['address']})")
            
        if devices:
            # select a device to connect 
            choice = int(input("\nPlease select the device type to connect (1 battery- 2 controller):"))
            if 1 <= choice <= len(choices):
                selected_type = choices[choice - 1]
            else:
                print("Input out of range, please try again")
                return
            while True:         
                try:
                    choice = int(input("\nPlease enter the device number to connect (1-{}): ".format(len(devices))))
                    if 1 <= choice <= len(devices):
                        selected_device = devices[choice - 1]
                        break
                    else:
                        print("Input out of range, please try again")
                except ValueError:
                    print("Invalid input, please enter a number")
            
            success = await client.connect(selected_device['address'])
            connected = success
            print(f"\nconnect status: {'success' if success else 'failture'}")
            
            if success:
                while True:
                    # send read command: get data
                    print("get data")
                    response = await client.get_hole_original_data(DeviceType=selected_type)
                    print(response)

                    # send write command: set data
                    print("get status")
                    response = await client.get_status(DeviceType=selected_type)
                    print(response)
                    choice = int(input("continue or exit? 1.continue 2.exit\n"))
                    if choice==1:
                        continue
                    else:
                        break
    except Exception as e:
        print(f"catch exception:{str(e)}")
    finally:
            if connected:
                await client.disconnect()
    
if __name__ == "__main__":
    asyncio.run(main())
```
## Features
- Device Scanning : Use the scan_devices method to scan nearby Bluetooth devices.
- Device Connection : Use the connect method to connect to the selected device.
- Data Retrieval : Use the get_hole_original_data and get_status methods to obtain raw data and status information from the device.

## License
This project is licensed under the Renogy License. For more details, please refer to the https://www.renogy.com.