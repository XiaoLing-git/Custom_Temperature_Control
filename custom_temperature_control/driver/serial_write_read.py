"""SerialWriteRead."""

import logging
import time

from ..utils import assert_hex_code, modbus_crc16
from .serial_connection import SerialConnection

logger = logging.getLogger(__name__)


class SerialWriteRead(SerialConnection):
    """
    SerialWriteRead
    """

    def write(self, cmd: str) -> None:
        """
        write cmd code
        :param cmd:
        :return:
        """
        assert_hex_code(cmd)
        logger.debug(f"Write: {cmd}")
        try:
            self._ser.write(bytes.fromhex(cmd))
        except Exception as e:
            raise ValueError(f"Write Command:{cmd} Fail {e}")

    def __read(self) -> str:
        buffer_length: int = self._ser.in_waiting
        if buffer_length == 0:
            return ""
        else:
            try:
                response: str = self._ser.read(buffer_length).hex()
            except Exception as e:
                raise ValueError(f"Serial Read Exception Happened {e}")
            return response.upper()

    def read_size(self, size: int, timeout: float) -> str:
        """
        Read a certain amount of bytes
        :param size:
        :param timeout:
        :return:
        """
        start_time: float = time.time()
        response: str = ""
        while True:
            duration: float = time.time() - start_time
            if duration > timeout:
                break
            response = response + self.__read()
            if len(response) == size:
                break
        current_size = len(response)
        if current_size != size:
            raise ValueError(f"Serial read timeout error, Current Size = {current_size} Timeout={timeout}")
        logger.debug(f" ReadSize: Size = {current_size}, Response = {response}")
        return response

    def read(self, timeout: float = 2) -> str:
        """
        Read until get something
        :param timeout:
        :return:
        """
        time.sleep(0.1)
        start_time: float = time.time()
        response: str = ""
        while True:
            duration: float = time.time() - start_time
            _length: int = len(response)
            if duration > timeout:
                raise ValueError(f"Serial read timeout, " f"Response = {response}, " f"Timeout={timeout}")
            response = response + self.__read()
            if _length < 4:
                continue
            content: str = response[:-4]
            crc16: str = response[-4:]
            if modbus_crc16(content) == crc16:
                break
        logger.debug(f" Read: {response}")
        logger.debug("-" * 100)
        return response
