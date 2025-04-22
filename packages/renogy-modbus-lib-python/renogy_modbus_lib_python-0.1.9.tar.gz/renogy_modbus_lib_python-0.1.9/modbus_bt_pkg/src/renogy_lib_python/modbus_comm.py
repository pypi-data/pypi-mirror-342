from .cal_tools import calculate_crc,verify_crc,hex_to_ascii,process_res
from bleak import BleakClient
from bleak.exc import BleakError
from bleak import BleakScanner
import asyncio
from typing import Optional
from collections import deque
from .battery_protocol import battery,Status1,Status2,Status3,Cell_voltage_Alarminfo,Cell_Temperature_Alarminfo,Other_Alarminfo,Charge_Discharge_status
from .controller_protocol import controller,C_Status1,C_Status2
from dataclasses import asdict
class modbus_comm:
    def __init__(self,write_service_uuid: str = "0000ffd0-0000-1000-8000-00805f9b34fb",
        write_char_uuid: str = "0000ffd1-0000-1000-8000-00805f9b34fb",
        notify_service_uuid: str = "0000fff0-0000-1000-8000-00805f9b34fb",
        notify_char_uuid: str = "0000fff1-0000-1000-8000-00805f9b34fb",
        slave_address: int = 1,
        timeout: float = 3.0) -> None:
        self.write_service_uuid = write_service_uuid
        self.write_char_uuid = write_char_uuid
        self.notify_service_uuid = notify_service_uuid
        self.notify_char_uuid = notify_char_uuid
        self.slave_address = slave_address
        self.timeout = timeout
        
        self.client: Optional[BleakClient] = None
        self.response_queue = deque()
        self.lock = asyncio.Lock()
        self.expected_length = 0
        # write characteristic cache
        self.write_char = None  
        # notify characteristic cache
        self.notify_char = None  

    async def scan_devices(self):
        """Scan and return a list of eligible BLE devices"""
        print("Scanning BLE devices (for 10 seconds)...")
        # device storage array
        self.valid_devices = []  
        try:
            devices = await BleakScanner.discover(timeout=10)
            
            for d in devices:
                if d.name and (d.name.startswith('RNG') or d.name.startswith('BT')):
                    print(f"found eligible BLE devices: {d.name} | address: {d.address} | rssi: {d.rssi}")
                    self.valid_devices.append({  
                        'name': d.name,
                        'address': d.address
                    })
                else:
                    print(f"Filter out non-target device: {d.name} | address: {d.address}")
            return self.valid_devices 
        except BleakError as e:
            print(str(e))
            return []

    async def connect(self, device_address:str) -> bool:
        """Connection method that returns connection status"""
        try:
            self.client = BleakClient(device_address)
            # Connection with timeout
            await asyncio.wait_for(self.client.connect(), timeout=10.0)
            
            # Get the write service and correct characteristic
            write_service = self.client.services.get_service(self.write_service_uuid)
            self.write_char = write_service.get_characteristic(self.write_char_uuid)
            
            # Get the notify service and find the correct characteristic
            service = self.client.services.get_service(self.notify_service_uuid)
            self.notify_char = service.get_characteristic(self.notify_char_uuid)

            # Enable notification subscription (using the characteristic handle)
            await self.client.start_notify(
                self.notify_char.handle,  # Use the characteristic handle instead of UUID
                self._notification_handler
            )
            print("Connected and notification enabled")
            
            # Enhanced characteristic property check
            if not self.write_char:
                raise RuntimeError(f"not found write characterister {self.write_char_uuid}")
            if not self.write_char.properties:
                raise RuntimeError("write characterister not defined")
            self.connected = False    
            return True
            
        except BleakError as e:
            print(f"connection failture: {str(e)}")
            return False
        except asyncio.TimeoutError:
            print("connection timeout")
            return False
        except Exception as e:
            print(f"unknown connection error: {str(e)}")
            return False

    async def disconnect(self):
        if self.client and self.client.is_connected:
            # Use the characteristic handle obtained during the previous connection
            if hasattr(self, 'notify_char'):
                await self.client.stop_notify(self.notify_char.handle)
            await self.client.disconnect()
            print("Disconnected")

    def _notification_handler(self,sender,data:bytearray):
        """Callback function to handle BLE notification data"""
        # print(f"收到原始响应: {data.hex()}")  # 新增原始数据日志
        try:
            # Check address 
            if data[0] != self.slave_address:
                return
            # CRC verify
            if not verify_crc(data):
                print("crc verify failture,dropped the data")
                return
            self.response_queue.append(data)
        except BleakError as e:
            print(e)

    async def _send_request(self,pdu_data:bytes,flag:bool=False) -> bytes:
        """Send request and wait for response"""
        # Construct complete frame command: address PDU command CRC
        async with self.lock:
            frame  = (self.slave_address.to_bytes(1,'big')+pdu_data)
            frame += calculate_crc(frame)
            # Clear old responses
            self.response_queue.clear()

            # Check characteristic properties
            if self.write_char is None:
                raise RuntimeError("Write characteristic not initialized")
                
            # Select write method based on characteristic properties
            if 'write-without-response' in self.write_char.properties:
                write_method = self.client.write_gatt_char
                response_flag = False
            elif 'write' in self.write_char.properties:
                write_method = self.client.write_gatt_char
                response_flag = True
            else:
                raise RuntimeError("Characteristic does not support write operation")
            
            try:
                await write_method(
                    self.write_char.handle,
                    frame,
                    response=response_flag
                )
            except BleakError as e:
                print(f"write failed: {str(e)}")
                raise
                
            # print(f"send data: {frame.hex()}")

            # wait response, write mode return directly
            if flag:
                return True
            try:
                return await asyncio.wait_for(
                    self._wait_for_response(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                print(f"超时发生时响应队列内容: {self.response_queue}")
                raise

    async def _wait_for_response(self) -> bytes:
        """Get response data from the notification queue"""
        while True:
            if self.response_queue:
                response = self.response_queue.popleft()
                return response
            await asyncio.sleep(0.1)
    
    async def read_holding_registers(
        self,
        start_address: int,
        register_count: int
    ) -> bytes:
        """Read holding registers optimized implementation (returns raw byte data)"""
        pdu = bytes([
            0x03,  # Function code
            (start_address >> 8) & 0xFF,
            start_address & 0xFF,
            (register_count >> 8) & 0xFF,
            register_count & 0xFF
        ])
        response = await self._send_request(pdu)
        
        # Parse response
        if response[1] not in [0x03,0x06]:
            raise ValueError(f"Invalid function code response: {response[1]:02x}")
        
        # Directly return the data part of the bytes (excluding address, function code, byte count, and CRC)
        # Response structure: [address][function code][byte count][data...][CRC]
        return bytes(response[3:-2])  

    async def write_single_register(
        self,
        register_address: int,
        value: int
    ) -> bool:
        """write single register"""
        pdu = bytes([
            0x06,  # function code
            (register_address >> 8) & 0xFF,
            register_address & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        try:
            return await self._send_request(pdu,True)
            # Verify response frame structure
        except Exception as e:
            print(f"Write failed: {str(e)}")
            return False

class EnhancedModbusClient(modbus_comm):
    """Enhanced client with automatic reconnection mechanism"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reconnect_flag = False
        
    async def safe_send(self, method, *args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except BleakError as e:
            print(f"communication error: {str(e)},try reconnect...")
            await self._reconnect()
            return await method(*args, **kwargs)
            
    async def _reconnect(self):
        if self.client and self.client.is_connected:
            await self.disconnect()
        await self.connect(self.client.address)
    
    # isController
    async def is_controller(self):
        ctl = controller()
        pdu,count,_ = ctl.DeviceType
        try:
            res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                            register_count=count)
            print(f"DeviceType:{res.hex()}")
            if res.hex() == '0000' or res.hex() == '0001':
                return True
        except Exception:
                return False
        
    # isBattery
    async def is_battery(self):
        bat = battery()
        pdu,count,_ = bat.Battery_name
        try:
            res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                                register_count=count)
            print(f"Battery_name:{res.hex()}")
            if '4254' in res.hex():
                return True
        except Exception:
                return False
    # Get open data
    async def get_hole_original_data(self,DeviceType:str):
        if DeviceType == "battery":
            bat = battery()
            result =[]
            for key,value in asdict(bat).items():
                pdu, count, multiplier = value
                res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                            register_count=count)
                await asyncio.sleep(0.2)
                # print(f"{key}值为{res.hex()}")
                if key=="Lock_ControL":
                    result.append({key:'Lock' if res == 0x5a5a else 'Unlock'})
                elif key=="Test_Ready":
                    result.append({key:'Test begin' if res == 0x5a5a else 'Test over'})
                elif key=="Battery_name":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="SN_Number":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Software_Version":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Manufacture_version":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Manufacturer_Name":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Main_line_version":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Communication_protocol_version":
                    result.append({key:hex_to_ascii(res.hex())})
                else:
                    result.append({key:int.from_bytes(res,'big') * multiplier})
            return result
        elif DeviceType == "controller":
            ctl = controller()
            result =[]
            for key,value in asdict(ctl).items():
                pdu, count, multiplier = value
                res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                            register_count=count)
                await asyncio.sleep(0.2)
                if key=="Rated_Voltage_Current":
                    res_int = int.from_bytes(res,'big')
                    Highest_voltage = res_int >> 8 & 0xff * multiplier
                    Highest_current =  res_int & 0xff * multiplier
                    result.append({key:f"{Highest_voltage}V-{Highest_current}A"})
                elif key=="DeviceType":
                    result.append({key:res.hex()})
                elif key=="SKU":
                    result.append({key:hex_to_ascii(res.hex())})
                elif key=="Software_Version":
                    result.append({key:res.hex()})
                elif key=="Hardware_Version":
                    result.append({key:res.hex()})
                elif key=="DeviceAddress":
                    result.append({key:res.hex()})
                elif key=="Protocol_Version":
                    result.append({key:res.hex()})
                elif key=="Device_ID":
                    result.append({key:res.hex()})
                elif key=="SN_Number":
                    result.append({key:res.hex()})
                elif key=="Status1" or key=="Status2":
                    continue
                else:
                    result.append({key:int.from_bytes(res,'big') * multiplier})
            return result
        else:
            print("DeviceType is not support")
            return False

    
    # Get alarm
    # async def get_alarms(self):
    #     bat = battery()
    #     result=[]
    #     alarm_list = [{'Cell_voltage_Alarminfo':bat.Cell_voltage_Alarminfo},{'Cell_Temperature_Alarminfo':bat.Cell_Temperature_Alarminfo},
    #                  {'Other_Alarminfo':bat.Other_Alarminfo}]
    #     for alarm in alarm_list:
    #         message,tuple = next(iter(alarm.items()))
    #         pdu,count,_ = tuple
    #         res = await self.safe_send(self.read_holding_registers,start_address=pdu,
    #                             register_count=count)
    #         print(res.hex())
    #         if res.hex() != '00000000':
    #             result.append({message:'alarm'}) 
    #         else:
    #             result.append({message:'normal'}) 
    #     return result
    
    # Get status
    async def get_status(self,DeviceType:str):
        if DeviceType == "battery":
            bat = battery()
            st1 = Status1()
            st2 = Status2()
            st3 = Status3()
            st4 = Cell_voltage_Alarminfo()
            st5 = Cell_Temperature_Alarminfo()
            st6 = Other_Alarminfo()
            st7 = Charge_Discharge_status()
            result = []
            status_list = [{st1: bat.Status1}, {st2: bat.Status2}, {st3: bat.Status3}, {st4: bat.Cell_voltage_Alarminfo},
                        {st5: bat.Cell_Temperature_Alarminfo}, {st6: bat.Other_Alarminfo},
                        {st7: bat.Charge_Discharge_status}]
            
            for status in status_list:
                st,tuple = next(iter(status.items()))
                pdu,count,_ = tuple
                res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                                    register_count=count)
                value = int.from_bytes(res,byteorder="big")
                (res := st.check_status(value)) and result.append(res)
            return result
        elif DeviceType == "controller":
            ctl = controller()
            st1 = C_Status1()
            st2 = C_Status2()
            result = []
            status_list = [{st1: ctl.Status1}, {st2: ctl.Status2}]

            for status in status_list:
                st,tuple = next(iter(status.items()))
                pdu,count,_ = tuple
                res = await self.safe_send(self.read_holding_registers,start_address=pdu,
                                    register_count=count)
                value = int.from_bytes(res,byteorder="big")
                (res := st.check_status(value)) and result.append(res)
            return result
        else:
            print("DeviceType is not support")
            return False