""""""

import logging
from typing import Any

from ..models import CommandCode, ControlMode, ControlStatus, ErrorCode, ResponseCode, RunStatus
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
        if len(data) == 0:
            cmd_str = f"{self.device_type}{self.device_number}{cmd.value}{str_length}"
        else:
            cmd_str = f"{self.device_type}{self.device_number}{cmd.value}{str_length}{data}"

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

    def get_status(self) -> dict[str, Any]:
        """TODO"""
        response = self.__send_cmd(CommandCode.GET_STATUS)
        response_bytes = bytes.fromhex(response)

        error_code = ErrorCode.get_value(response_bytes[4])
        run_status = RunStatus.get_value(response_bytes[5])
        control_status = ControlStatus.get_status(response_bytes[6])
        control_mode = ControlMode.get_mode(response_bytes[6])

        duration = int.from_bytes(bytes.fromhex(response[14:18]), byteorder="big")
        temperature = int.from_bytes(bytes.fromhex(response[18:22]), byteorder="big") / 10
        setup_temperature = int.from_bytes(bytes.fromhex(response[22:26]), byteorder="big") / 10
        return {
            "error_code": error_code,
            "run_status": run_status,
            "control_status": control_status,
            "control_mode": control_mode,
            "duration": duration,
            "temperature": temperature,
            "setup_temperature": setup_temperature,
        }

    def enable(
        self,
        temperature: float | None = None,
        duration: int = 0,
        control_status: ControlStatus = ControlStatus.running,
        control_mode: ControlMode = ControlMode.normal,
    ) -> str:
        """TODO"""
        if temperature is None:
            current_temperature = self.get_status().get("temperature")
            assert current_temperature is not None
            temperature = current_temperature

        assert -100 <= temperature <= 1050
        assert 0 <= duration <= 65535
        status = int.to_bytes((control_status.value | control_mode.value), byteorder="big", length=1).hex()
        format_temp = int.to_bytes(int(temperature * 10), byteorder="big", length=2).hex()
        format_duration = int.to_bytes(duration, byteorder="big", length=2).hex()
        response = self.__send_cmd(CommandCode.ENABLE, f"{status}{format_duration}{format_temp}".upper())
        return response

    def disable(self) -> str:
        """TODO"""
        response = self.__send_cmd(CommandCode.DISABLE)
        return response
