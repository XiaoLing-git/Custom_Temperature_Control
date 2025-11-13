"""Main function entry, mainly used for debugging."""
from opentrons.protocol_api import ProtocolContext

from custom_temperature_control.ot2_driver import Ot2Driver

# import logging
# import time
#
# from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial
#
# from custom_temperature_control.driver import Driver
# from custom_temperature_control.driver.serial_connection import SerialConnection
# from custom_temperature_control.driver.serial_write_read import SerialWriteRead
# from custom_temperature_control.models import ResponseCode
# from custom_temperature_control.ot2_driver import Ot2Driver
# from custom_temperature_control.utils import modbus_crc16, get_device_port

# logging.basicConfig(
#     level=logging.DEBUG,  # 核心：设置最低日志级别为DEBUG
#     format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
#     datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
# )
#
# if __name__ == "__main__":
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

    # modbus_crc16("58 01 A1 10 48 57 4D 4B 5F 48 43 5F 32 30 32 33 30 34 32 34")

    # ser = Ot2Driver()
    # ser.connect()
    # res = ser.get_status()
    # print(res)
    #
    # ser.enable(25.5, 60)
    # while True:
    #     time.sleep(3)
    #     print(ser.get_status())
    #
    # res = get_device_port()
    # print(res)


metadata = {
    "contextName": "szdemo",
    "author": "Samuel@opentrons.com ",
    "description": "dsadasdasda",
}

# requirements
requirements = {"robotType": "Flex", "apiLevel": "2.21"}


def run(context: ProtocolContext):
    device = Ot2Driver(context)
    device.connect()
    res = device.get_status()
    context.comment(f"r{res}")

    device.enable(25.5, 60)

