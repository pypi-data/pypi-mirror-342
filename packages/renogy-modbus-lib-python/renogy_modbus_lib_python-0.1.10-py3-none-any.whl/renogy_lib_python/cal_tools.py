# CRC16计算封装
# 2025.02.10
# CC
def calculate_crc(data:bytes) -> bytes:
    """
    Modbus RTU CRC-16计算
    :param data: 输入字节数据
    :return: 2字节CRC校验码(小端序)
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            lsb = crc & 0x0001
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc.to_bytes(2,'little')

def verify_crc(data:bytes) -> bool:
    """
    验证数据帧CRC校验
    """
    if len(data) < 2:
        return False
    received_crc = data[-2:]
    calculated_crc = calculate_crc(data[:-2])
    return received_crc == calculated_crc

def hex_to_ascii(hex_string):
    # 去除首尾的空格
    hex_string = hex_string.strip()
    # 将16进制字符串转换为字节对象
    bytes_object = bytes.fromhex(hex_string)
    # 将字节对象解码为ASCII字符串
    ascii_string = bytes_object.decode('ascii', errors='ignore')
    return ascii_string.strip()


def process_res(res):
    # 如果输入不是字符串形式，则尝试直接处理
    if isinstance(res, int):
        hex_value = res
    else:
        # 确保输入是字符串
        res_str = str(res)

        # 检查是否已经有0x前缀
        if not res_str.startswith("0x"):
            # 如果没有0x前缀，则添加
            res_str = "0x" + res_str

        # 尝试将字符串转换为整数
        try:
            hex_value = int(res_str, 16)
        except ValueError:
            raise ValueError("Invalid input for hexadecimal conversion.")

    # 检查最高位是否为1，假设hex_value是一个16位的数
    if hex_value & 0x8000:
        # 如果最高位是1，执行hex_value - 0xffff - 1
        result = hex_value - 0xffff - 1
    else:
        # 否则，结果就是hex_value本身
        result = hex_value

    return result