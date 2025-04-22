from dataclasses import dataclass

@dataclass(frozen=True)
class controller():
    Rated_Voltage_Current               : tuple=(0x000A,1,1)
    DeviceType                          : tuple=(0x000B,1,1)
    SKU                                 : tuple=(0x000C,8,1)
    Software_Version                    : tuple=(0x0014,2,1)
    Hardware_Version                    : tuple=(0x0016,2,1)
    DeviceAddress                       : tuple=(0x001A,1,1)
    Protocol_Version                    : tuple=(0x001B,2,1)
    Device_ID                           : tuple=(0x001D,2,1)
    SN_Number                           : tuple=(0x001F,9,1)
    Battery_SOC                         : tuple=(0x0100,1,1)
    Battery_Voltage                     : tuple=(0x0101,1,0.1)
    Charge_Current                      : tuple=(0x0102,1,0.01)
    Generator_Voltage                   : tuple=(0x0104,1,0.1)
    Generator_Charge_Current            : tuple=(0x0105,1,0.01)
    Generator_Charge_Power              : tuple=(0x0106,1,1)
    Panel_Voltage                       : tuple=(0x0107,1,0.1)
    Panel_Current                       : tuple=(0x0108,1,0.01)
    Panel_Power                         : tuple=(0x0101,1,1)
    Daily_Power_Generation              : tuple=(0x0113,1,0.001)
    Total_Days                          : tuple=(0x0115,1,1)
    Total_Power_Generation              : tuple=(0x011C,2,0.001)
    Status1                             : tuple=(0x0120,1,1)
    Status2                             : tuple=(0x0121,2,1)

@dataclass(frozen=True)
class C_Status1():
    Not_Charge                          :int = 0b0000000000000000
    MPPT_Charge_Mode                    :int = 0b0000000000000010
    Balance_Charge_Mode                 :int = 0b0000000000000011
    Boost_Charge_Mode                   :int = 0b0000000000000100
    Float_Charge_Mode                   :int = 0b0000000000000101
    Limit_Current_Charge_Mode           :int = 0b0000000000000110
    DC_Charge_Mode                      :int = 0b0000000000000111

    def check_status(self,value:int):
        return {key: True for key in self.__dataclass_fields__.keys() if value & getattr(self, key)}

@dataclass(frozen=True)
class C_Status2():
    Panel_Input_OverVoltage             :int = 0b0000001000000000
    Fan_Alarm                           :int = 0b0000000100000000
    Panel_Input_OverPower               :int = 0b0000000010000000
    Battery_Over_Temperature            :int = 0b0000000001000000
    Controller_OverTemperature          :int = 0b0000000000100000
    Battery_OverVoltage                 :int = 0b0000000000000010
    Battery_OverDischarge               :int = 0b0000000000000001

    def check_status(self,value:int):
        return {key: True for key in self.__dataclass_fields__.keys() if (value >> 16) & getattr(self, key)}