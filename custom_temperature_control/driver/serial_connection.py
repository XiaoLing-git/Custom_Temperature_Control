"""SerialConnect."""

import logging

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

logger = logging.getLogger(__name__)


class SerialConnection:
    """
    SerialConnection
    """

    __slots__ = (
        "__port",
        "__baud_rate",
        "__timeout",
        "__ser",
    )

    def __init__(self, port: str, baud_rate: int, timeout: float):
        """SerialConnection Init."""
        self.__port = port
        self.__baud_rate = baud_rate
        self.__timeout = timeout
        self.__ser: Serial | None = None

    @property
    def _ser(self) -> Serial:
        """Serial instance, for subclass."""
        if self.__ser is None:
            self.connect()
        assert self.__ser is not None
        if self.__ser.closed:
            self.connect()
        return self.__ser

    def connect(self) -> None:
        """connect to device."""
        if self.__ser is None:
            logger.debug(
                f"Connecting to device "
                f"port={self.__port} "
                f"baud_rate={self.__baud_rate} "
                f"timeout={self.__timeout}"
            )
            try:
                self.__ser = Serial(
                    port=self.__port,
                    baudrate=self.__baud_rate,
                    bytesize=EIGHTBITS,
                    stopbits=STOPBITS_ONE,
                    parity=PARITY_NONE,
                    timeout=self.__timeout,
                )
            except Exception as e:
                raise ValueError(
                    f"Device Connection Exception Happened "
                    f"port={self.__port} "
                    f"baud_rate={self.__baud_rate} "
                    f"timeout={self.__timeout} "
                    f"{e}"
                )
            logger.debug("Connecting to device success")
            return
        else:
            if self.__ser.closed:
                logger.debug(
                    f"Serial port closed, Reconnecting to device "
                    f"port={self.__port} "
                    f"baud_rate={self.__baud_rate} "
                    f"timeout={self.__timeout}"
                )
                try:
                    self.__ser.open()
                except Exception as e:
                    raise ValueError(
                        f"Device Reconnection Exception Happened "
                        f"port={self.__port} "
                        f"baud_rate={self.__baud_rate} "
                        f"timeout={self.__timeout} "
                        f"{e}"
                    )
                logger.debug("Reconnecting to device success")
                return
            else:

                logger.debug("Device connected already, No need do this again")
                return

    def disconnect(self) -> None:
        """disconnect from device."""
        if self.__ser is None:
            logger.debug(
                f"Serial instance not connected "
                f"port={self.__port} "
                f"baud_rate={self.__baud_rate} "
                f"timeout={self.__timeout}"
            )
            return
        else:
            if self.__ser.closed:
                logger.debug(
                    f"Serial port closed already no need do this again"
                    f"port={self.__port} "
                    f"baud_rate={self.__baud_rate} "
                    f"timeout={self.__timeout}"
                )
                return
            else:
                logger.debug(
                    f"Device disconnect"
                    f"port={self.__port} "
                    f"baud_rate={self.__baud_rate} "
                    f"timeout={self.__timeout}"
                )
                try:
                    self.__ser.close()
                except Exception as e:
                    raise ValueError(
                        f"Device Disconnection Exception Happened "
                        f"port={self.__port} "
                        f"baud_rate={self.__baud_rate} "
                        f"timeout={self.__timeout} "
                        f"{e}"
                    )
                logger.debug("Device disconnect success")
                return
