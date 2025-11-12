"""Main function entry, mainly used for debugging."""

import logging
import time

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

from custom_temperature_control.driver.serial_connection import SerialConnection
from custom_temperature_control.driver.serial_write_read import SerialWriteRead
from custom_temperature_control.utils import modbus_crc16

logging.basicConfig(
    level=logging.DEBUG,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

if __name__ == "__main__":
    # for port in [9600,14400,19200,38400,56000,57600,115200]:
    #     for addr in range(20):
    #         try:
    #             format_addr = int.to_bytes((addr+1),byteorder="big", length=1).hex()
    #             ser = SerialWriteRead(
    #                 port="COM13",
    #                 baud_rate=port,
    #                 timeout=10,
    #             )
    #             ser.connect()
    #             cmd = f"58{format_addr}0100".upper()
    #             cmd = cmd + modbus_crc16(cmd)
    #             ser.write(cmd)
    #             ser.read()
    #         except Exception as e:
    #             ser.disconnect()
    #             print(e)

    modbus_crc16("58 01 A1 10 48 57 4D 4B 5F 48 43 5F 32 30 32 33 30 34 32 34")

    ser = SerialWriteRead(
                    port="COM13",
                    baud_rate=9600,
                    timeout=10,
                )
    ser.connect()
    cmd = f"5801A000".upper()
    cmd = cmd + modbus_crc16(cmd)
    ser.write(cmd)
    ser.read()
