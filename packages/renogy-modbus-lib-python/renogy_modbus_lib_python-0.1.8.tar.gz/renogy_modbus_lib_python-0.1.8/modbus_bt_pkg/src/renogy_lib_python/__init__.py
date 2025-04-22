# 版本声明（推荐）
__version__ = "0.1.2"

# 导出模块中的特定内容（常用方式）
from .modbus_comm import (
    modbus_comm,
    EnhancedModbusClient
)

# 包初始化代码（可选）
print(f"Initializing {__name__} package")

# 定义 __all__ 控制 from package import * 的行为
__all__ = ['modbus_comm','EnhancedModbusClient']
