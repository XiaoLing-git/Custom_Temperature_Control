""""""

import logging

from ..models import CommandCode, ResponseCode
from ..utils import modbus_crc16
from .serial_write_read import SerialWriteRead

logger = logging.getLogger(__name__)


class Driver(SerialWriteRead):
    """TODO"""

    def __init__(
        self, port: str, baud_rate: int, timeout: float, device_type: str = "58", device_number: str = "01"
    ) -> None:
        """TODO"""
        super().__init__(port, baud_rate, timeout)
        self.device_type = device_type
        self.device_number = device_number

    def __send_cmd(self, cmd: CommandCode, data: str = "") -> str:
        """TODO"""
        _length = int(len(data) / 2)
        str_length = int.to_bytes(_length, byteorder="big", length=1).hex()

        cmd_str: str = f"{self.device_type}{self.device_number}{cmd.value}{str_length}"
        cmd_format = cmd_str + modbus_crc16(cmd_str)
        self.write(cmd_format)
        response = self.read()

        response_code = response[4:6]
        if response_code in ResponseCode.get_map(cmd.name):
            return response
        else:
            raise ValueError("命令解析异常")

    def get_version(self) -> str:
        """TODO"""
        response = self.__send_cmd(CommandCode.GET_VERSION)
        return response

    def restart(self) -> str:
        """TODO"""
        response = self.__send_cmd(CommandCode.RESTART)
        return response

    def get_status(self) -> str:
        """TODO"""

        cmd: str = f"{self.device_type}{self.device_number}0300"
        cmd_format = cmd + modbus_crc16(cmd)
        self.write(cmd_format)
        response = self.read()

        response_code = response[4:6]
        if response_code in ResponseCode.GET_VERSION.value:
            return ""
        else:
            raise ValueError("命令解析异常")
