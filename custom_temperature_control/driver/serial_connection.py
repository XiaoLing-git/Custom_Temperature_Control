""""""

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class SerialConnection:
    """SerialConnection"""

    def __init__(
        self,
        port: str,
        baud: int = 9600,
        bytesize: int = EIGHTBITS,
        stop_bits: float = STOPBITS_ONE,
        parity: str = PARITY_NONE,
        timeout: float = 0.1,
    ) -> None:
        """init"""
        self.port = port
        self.baud = baud
        self.bytesize = bytesize
        self.stop_bits = stop_bits
        self.parity = parity
        self.timeout = timeout
        self.__ser: Serial | None = None

    @property
    def serial(self) -> Serial | None:
        """serial"""
        return self.__ser

    def connect(self) -> None:
        """connect"""
        if self.serial is None:
            self.__ser = Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=self.timeout,
            )
        else:
            if self.serial.is_open:
                pass
            else:
                self.serial.open()

    def disconnect(self) -> None:
        """connect"""
        if self.__ser:
            if self.__ser.is_open:
                self.__ser.close()
                self.__ser = None
            else:
                return
        else:
            return
