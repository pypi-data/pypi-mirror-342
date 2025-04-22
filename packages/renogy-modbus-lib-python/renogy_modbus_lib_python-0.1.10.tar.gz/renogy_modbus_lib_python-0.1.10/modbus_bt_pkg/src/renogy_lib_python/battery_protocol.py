from dataclasses import dataclass
from enum import IntEnum

class CellValue(IntEnum):
    NORMAL = 0b00  # 正常
    BELOW_LOWER_LIMIT = 0b01  # 低于下限，触发保护
    ABOVE_HIGHER_LIMIT = 0b10  # 高于上限，触发保护
    OTHER_ALARM = 0b11  # 其他报警

@dataclass(frozen=True)
class battery():
    Number_of_Cell                      : tuple=(0x1388,1,1)
    Number_of_CellTemperature           : tuple=(0x1399,1,1)
    Temperature_of_BMS_board            : tuple=(0x13AB,1,0.1)
    Number_of_Environment_Temperature   : tuple=(0x13AC,1,1)
    Number_of_Heater_Temperature        : tuple=(0x13AF,1,1)
    Current                             : tuple=(0x13B2,1,0.1)
    Module_voltage                      : tuple=(0x13B3,1,0.1)
    Remain_capacity                     : tuple=(0x13B4,2,0.001)
    Module_total_capacity               : tuple=(0x13B6,2,0.001)
    Cycle_number                        : tuple=(0x13B8,1,1)
    Charge_voltage_limit                : tuple=(0x13B9,1,0.1)
    Discharge_voltage_limit             : tuple=(0x13BA,1,0.1)
    Charge_current_limit                : tuple=(0x13BB,1,0.01)
    Discharge_current_limit             : tuple=(0x13BC,1,0.01)
    Cell_voltage_Alarminfo              : tuple=(0x13EC,2,1)
    Cell_Temperature_Alarminfo          : tuple=(0x13EE,2,1)
    Other_Alarminfo                     : tuple=(0x13F0,2,1)
    Status1                             : tuple=(0x13F2,1,1)
    Status2                             : tuple=(0x13F3,1,1)
    Status3                             : tuple=(0x13F4,1,1)
    Charge_Discharge_status             : tuple=(0x13F5,1,1)
    Manufacture_version                 : tuple=(0x13FE,1,1)
    Main_line_version                   : tuple=(0x13FF,2,1)
    Communication_protocol_version      : tuple=(0x1401,1,1)
    Battery_name                        : tuple=(0x1402,8,1)
    Software_Version                    : tuple=(0x140A,2,1)
    Manufacturer_Name                   : tuple=(0x140C,10,1)
    Cell_over_voltage_limit             : tuple=(0x1450,1,0.1)
    Cell_high_voltage_limit             : tuple=(0x1451,1,0.1)
    Cell_low_voltage_limit              : tuple=(0x1452,1,0.1)
    Cell_under_voltage_limit            : tuple=(0x1453,1,0.1)
    Charge_over_temperature_limit       : tuple=(0x1454,1,0.1)
    Charge_high_temperature_limit       : tuple=(0x1455,1,0.1)
    Charge_low_temperature_limit        : tuple=(0x1456,1,0.1)
    Charge_under_temperature_limit      : tuple=(0x1457,1,0.1)
    Charge_over2_current_limit          : tuple=(0x1458,1,0.01)
    Charge_over1_current_limit          : tuple=(0x1459,1,0.01)
    Charge_high_current_limit           : tuple=(0x145A,1,0.01)
    Module_over_voltage_limit           : tuple=(0x145B,1,0.1)
    Module_high_voltage_limit           : tuple=(0x145C,1,0.1)
    Module_low_voltage_limit            : tuple=(0x145D,1,0.1)
    Module_under_voltage_limit          : tuple=(0x145E,1,0.1)
    Discharge_over                      : tuple=(0x145F,1,0.1)
    Discharge_high_temperature_limit    : tuple=(0x1460,1,0.1)
    Discharge_low_temperature_limit     : tuple=(0x1461,1,0.1)
    Discharge_under_temperature_limit   : tuple=(0x1462,1,0.1)
    Discharge_over2_current_limit       : tuple=(0x1463,1,0.01)
    Discharge_over1_current_limit       : tuple=(0x1464,1,0.01)
    Discharge_high_current_limit        : tuple=(0x1465,1,0.01)
    Shutdown_command                    : tuple=(0x1466,1,1)
    Device_ID                           : tuple=(0x1467,1,1)
    Lock_ControL                        : tuple=(0x1468,1,1)
    Test_Ready                          : tuple=(0x1469,1,1)
    Unique_identification_code          : tuple=(0x146A,2,1)
    SN_Number                           : tuple=(0x146C,9,1)

@dataclass(frozen=True)
class Status1():
    Module_under_voltage                :int = 0b1000000000000000
    Charge_over_temp                    :int = 0b0100000000000000
    Charge_under_temp                   :int = 0b0010000000000000
    Discharge_over_temp                 :int = 0b0001000000000000
    Discharge_under_temp                :int = 0b0000100000000000
    Discharge_over_current1             :int = 0b0000010000000000
    Charge_over_current1                :int = 0b0000001000000000
    Cell_over_voltage                   :int = 0b0000000100000000
    Cell_under_voltage                  :int = 0b0000000010000000
    Module_over_voltage                 :int = 0b0000000001000000
    Discharge_over_current_2            :int = 0b0000000000100000
    Charge_over_current_2               :int = 0b0000000000010000
    Using_battery_module_power          :int = 0b0000000000001000
    Discharge                           :int = 0b0000000000000100
    Charge_MOSFET                       :int = 0b0000000000000010
    short_circuit                       :int = 0b0000000000000001
    
    def check_status(self,value:int):
        return {key: True for key in self.__dataclass_fields__.keys() if value & getattr(self, key)}
    
@dataclass(frozen=True)
class Status2():
    Effective_charge_current            :int = 0b1000000000000000
    Effective_discharge_current         :int = 0b0100000000000000
    Heater_on                           :int = 0b0010000000000000
    Reserve1                             :int = 0b0001000000000000
    Fully_charged                       :int = 0b0000100000000000
    Reserve2                             :int = 0b0000010000000000
    Reserve3                             :int = 0b0000001000000000
    Buzzer                              :int = 0b0000000100000000
    Discharge_high_temp                 :int = 0b0000000010000000
    Discharge_low_temp                  :int = 0b0000000001000000
    Charge_high_temp                    :int = 0b0000000000100000
    Charge_low_temp                     :int = 0b0000000000010000
    Module_high_voltage                 :int = 0b0000000000001000
    Module_low_voltage                  :int = 0b0000000000000100
    Cell_high_voltage                   :int = 0b0000000000000010
    Cell_low_voltage                    :int = 0b0000000000000001
    
    def check_status(self,value:int):
        return {key: True for key in self.__dataclass_fields__.keys() if value & getattr(self, key)}

@dataclass(frozen=True)
class Status3():
    Cell_votage16                       :int = 0b1000000000000000
    Cell_votage15                       :int = 0b0100000000000000
    Cell_votage14                       :int = 0b0010000000000000
    Cell_votage13                       :int = 0b0001000000000000
    Cell_votage12                       :int = 0b0000100000000000
    Cell_votage11                       :int = 0b0000010000000000
    Cell_votage10                       :int = 0b0000001000000000
    Cell_votage9                        :int = 0b0000000100000000
    Cell_votage8                        :int = 0b0000000010000000
    Cell_votage7                        :int = 0b0000000001000000
    Cell_votage6                        :int = 0b0000000000100000
    Cell_votage5                        :int = 0b0000000000010000
    Cell_votage4                        :int = 0b0000000000001000
    Cell_votage3                        :int = 0b0000000000000100
    Cell_votage2                        :int = 0b0000000000000010
    Cell_votage1                        :int = 0b0000000000000001
    
    # def check_status(self,value:int):
    #     return {key: True for key in self.__dataclass_fields__.keys() if value & getattr(self, key)}

    def get_state_flags(self, value: int) -> dict:
        """
        获取所有状态的值（1: Error, 0: Normal）。
        :param value: 8 位的状态值
        :return: 包含所有状态及其值的字典
        """
        return {
            key: "Error" if value & getattr(self, key) else "Normal"
            for key in self.__dataclass_fields__.keys()
        }

    def check_status(self, value: int) -> dict:
        """
        将所有状态值汇总到 Status3 字段。
        :param value: 8 位的状态值
        :return: 包含 Status3 的字典
        """
        state_flags = self.get_state_flags(value)
        return {
            "Status3": state_flags
        }


@dataclass(frozen=True)
class Cell_voltage_Alarminfo():
    # 每两位表示一个状态
    Cell1: int = 0b00000000000000000000000000000011  # 最低两位 (bits 0-1)
    Cell2: int = 0b00000000000000000000000000001100  # bits 2-3
    Cell3: int = 0b00000000000000000000000000110000  # bits 4-5
    Cell4: int = 0b00000000000000000000000011000000  # bits 6-7
    Cell5: int = 0b00000000000000000000001100000000  # bits 8-9
    Cell6: int = 0b00000000000000000000110000000000  # bits 10-11
    Cell7: int = 0b00000000000000000011000000000000  # bits 12-13
    Cell8: int = 0b00000000000000001100000000000000  # bits 14-15
    Cell9: int = 0b00000000000000110000000000000000  # bits 16-17
    Cell10: int = 0b00000000000011000000000000000000  # bits 18-19
    Cell11: int = 0b00000000001100000000000000000000  # bits 20-21
    Cell12: int = 0b00000000110000000000000000000000  # bits 22-23
    Cell13: int = 0b00000011000000000000000000000000  # bits 24-25
    Cell14: int = 0b00001100000000000000000000000000  # bits 26-27
    Cell15: int = 0b00110000000000000000000000000000  # bits 28-29
    Cell16: int = 0b11000000000000000000000000000000  # 最高两位 (bits 30-31)

    def get_state_meaning(self, value: int) -> dict:
        """
        获取所有状态的具体含义。
        :param value: 32 位的状态值
        :return: 包含所有状态及其含义的字典
        """
        return {
            key: CellValue((value & getattr(self, key)) >> shift).name
            for key in self.__dataclass_fields__.keys()
            for shift in [(getattr(self, key) & -getattr(self, key)).bit_length() - 1]
        }
    def check_status(self, value: int) -> dict:
        """
        将所有状态值汇总到 Cell_voltage_Alarminfo 字段。
        :param value: 32 位的状态值
        :return: 包含 Cell_voltage_Alarminfo 的字典
        """
        state_meanings = self.get_state_meaning(value)
        return {
            "Cell_voltage_Alarminfo": state_meanings
        }

@dataclass(frozen=True)
class Cell_Temperature_Alarminfo():
    # 每两位表示一个状态
    Temperature_of_cell_1: int = 0b00000000000000000000000000000011  # 最低两位 (bits 0-1)
    Temperature_of_cell_2: int = 0b00000000000000000000000000001100  # bits 2-3
    Temperature_of_cell_3: int = 0b00000000000000000000000000110000  # bits 4-5
    Temperature_of_cell_4: int = 0b00000000000000000000000011000000  # bits 6-7
    Temperature_of_cell_5: int = 0b00000000000000000000001100000000  # bits 8-9
    Temperature_of_cell_6: int = 0b00000000000000000000110000000000  # bits 10-11
    Temperature_of_cell_7: int = 0b00000000000000000011000000000000  # bits 12-13
    Temperature_of_cell_8: int = 0b00000000000000001100000000000000  # bits 14-15
    Temperature_of_cell_9: int = 0b00000000000000110000000000000000  # bits 16-17
    Temperature_of_cell_10: int = 0b00000000000011000000000000000000  # bits 18-19
    Temperature_of_cell_11: int = 0b00000000001100000000000000000000  # bits 20-21
    Temperature_of_cell_12: int = 0b00000000110000000000000000000000  # bits 22-23
    Temperature_of_cell_13: int = 0b00000011000000000000000000000000  # bits 24-25
    Temperature_of_cell_14: int = 0b00001100000000000000000000000000  # bits 26-27
    Temperature_of_cell_15: int = 0b00110000000000000000000000000000  # bits 28-29
    Temperature_of_cell_16: int = 0b11000000000000000000000000000000  # 最高两位 (bits 30-31)

    def get_state_meaning(self, value: int) -> dict:
        """
        获取所有状态的具体含义。
        :param value: 32 位的状态值
        :return: 包含所有状态及其含义的字典
        """
        return {
            key: CellValue((value & getattr(self, key)) >> shift).name
            for key in self.__dataclass_fields__.keys()
            for shift in [(getattr(self, key) & -getattr(self, key)).bit_length() - 1]
        }
    def check_status(self, value: int) -> dict:
        """
        将所有状态值汇总到 Cell_Temperature_Alarminfo 字段。
        :param value: 32 位的状态值
        :return: 包含 Cell_Temperature_Alarminfo 的字典
        """
        state_meanings = self.get_state_meaning(value)
        return {
            "Cell_Temperature_Alarminfo": state_meanings
        }

@dataclass(frozen=True)
class Other_Alarminfo():
    # 每两位表示一个状态
    Reserve1: int = 0b00000000000000000000000000000011  # 最低两位 (bits 0-1)
    Reserve2: int = 0b00000000000000000000000000001100  # bits 2-3
    Reserve3: int = 0b00000000000000000000000000110000  # bits 4-5
    Reserve4: int = 0b00000000000000000000000011000000  # bits 6-7
    Reserve5: int = 0b00000000000000000000001100000000  # bits 8-9
    Reserve6: int = 0b00000000000000000000110000000000  # bits 10-11
    Reserve7: int = 0b00000000000000000011000000000000  # bits 12-13
    Reserve8: int = 0b00000000000000001100000000000000  # bits 14-15
    Reserve9: int = 0b00000000000000110000000000000000  # bits 16-17
    Discharge_current: int = 0b00000000000011000000000000000000  # bits 18-19
    Charge_current: int = 0b00000000001100000000000000000000  # bits 20-21
    HeaterTemperature_2: int = 0b00000000110000000000000000000000  # bits 22-23
    HeaterTemperature_1: int = 0b00000011000000000000000000000000  # bits 24-25
    Reserve_EnvironmentTemperature_2: int = 0b00001100000000000000000000000000  # bits 26-27
    Reserve_EnvironmentTemperature_1: int = 0b00110000000000000000000000000000  # bits 28-29
    Temperature_of_BMS_board: int = 0b11000000000000000000000000000000  # 最高两位 (bits 30-31)

    def get_state_meaning(self, value: int) -> dict:
        """
        获取所有状态的具体含义。
        :param value: 32 位的状态值
        :return: 包含所有状态及其含义的字典
        """
        return {
            key: CellValue((value & getattr(self, key)) >> shift).name
            for key in self.__dataclass_fields__.keys()
            for shift in [(getattr(self, key) & -getattr(self, key)).bit_length() - 1]
        }
    def check_status(self, value: int) -> dict:
        """
        将所有状态值汇总到 Other_Alarminfo 字段。
        :param value: 32 位的状态值
        :return: 包含 Other_Alarminfo 的字典
        """
        state_meanings = self.get_state_meaning(value)
        return {
            "Other_Alarminfo": state_meanings
        }

@dataclass(frozen=True)
class Charge_Discharge_status:
    # 每个 bit 表示一个状态
    Reserve1: int = 0b00000001  # 最低位 (bit 0)
    Reserve2: int = 0b00000010  # bit 1
    Reserve3: int = 0b00000100  # bit 2
    Fullcharge_request: int = 0b00001000  # bit 3
    Charge_immediately2: int = 0b00010000  # bit 4
    Charge_immediately1: int = 0b00100000  # bit 5
    Discharge_enable: int = 0b01000000  # bit 6
    Charge_enable: int = 0b10000000  # 最高位 (bit 7)

    def get_state_flags(self, value: int) -> dict:
        """
        获取所有状态的值。
        - bit 0-5: 1: yes, 0: normal
        - bit 6-7: 0: Request stop charge, 1: Yes
        :param value: 8 位的状态值
        :return: 包含所有状态及其值的字典
        """
        state_flags = {}
        for key in self.__dataclass_fields__.keys():
            mask = getattr(self, key)
            if key in ["Discharge_enable", "Charge_enable"]:  # 处理 bit 6 和 bit 7
                state_flags[key] = "Request stop charge" if (value & mask) == 0 else "Yes"
            else:  # 处理 bit 0-5
                state_flags[key] = "yes" if value & mask else "normal"
        return state_flags

    def check_status(self, value: int) -> dict:
        """
        将所有状态值汇总到 Charge_Discharge_status 字段。
        :param value: 8 位的状态值
        :return: 包含 Charge_Discharge_status 的字典
        """
        state_flags = self.get_state_flags(value)
        return {
            "Charge_Discharge_status": state_flags
        }