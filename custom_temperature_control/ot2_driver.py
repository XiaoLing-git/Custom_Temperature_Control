"""TODO"""

from typing import Any

from opentrons.protocol_api import ProtocolContext

from .driver import Driver
from .models import ControlMode, ControlStatus, ErrorCode, RunStatus


class Ot2Driver:
    """TODO"""

    def __init__(self, port: str, baud_rate: int, timeout: float, context: ProtocolContext) -> None:
        """TODO"""
        self.__device = Driver(port, baud_rate, timeout)
        self.__simulate: bool = context.is_simulating()
        self.__context = context

    @property
    def device(self) -> Driver:
        """TODO"""
        return self.__device

    @property
    def context(self) -> ProtocolContext:
        """TODO"""
        return self.__context

    @property
    def simulate(self) -> bool:
        """TODO"""
        return self.__simulate

    def connect(self) -> None:
        """TODO"""
        self.context.comment(
            f"Device Connect "
            f"port: {self.device.port} "
            f"baud_rate:{self.device.baud_rate} "
            f"timeout: {self.device.timeout}"
        )

        if self.simulate:
            return
        else:
            self.device.connect()

    def disconnect(self) -> None:
        """TODO"""
        self.context.comment(
            f"Device Disconnect "
            f"port: {self.device.port} "
            f"baud_rate:{self.device.baud_rate} "
            f"timeout: {self.device.timeout}"
        )

        if self.simulate:
            return
        else:
            self.device.disconnect()

    def get_version(self) -> str:
        """TODO"""
        self.context.comment(f"Send |Get_Device_Version| Command")

        if self.simulate:
            return "Device_Version"
        else:
            return self.device.get_version()

    def restart(self) -> str:
        """TODO"""
        self.context.comment(f"Send |Restart| Command")

        if self.simulate:
            return "Restart"
        else:
            return self.device.restart()

    def get_status(self) -> dict[str, Any]:
        """TODO"""
        self.context.comment(f"Send |Get_Device_Status| Command")

        if self.simulate:
            return {
                "error_code": ErrorCode.normal,
                "run_status": RunStatus.idle,
                "control_status": ControlStatus.running,
                "control_mode": ControlMode.normal,
                "duration": 0,
                "temperature": 27,
                "setup_temperature": 27,
            }
        else:
            return self.device.get_status()

    @property
    def run_status(self) -> RunStatus:
        """TODO"""
        status = self.get_status()
        run_status = status["run_status"]
        assert isinstance(run_status, RunStatus)
        self.context.comment(f"Current Run Status: {run_status.name}")
        return run_status

    @property
    def current_temperature(self) -> float:
        """TODO"""
        status = self.get_status()
        value = status["temperature"]
        self.context.comment(f"Current Run Temperature: {value}C")
        return float(value)

    @property
    def hold_time(self) -> int:
        """TODO"""
        status = self.get_status()
        value = status["duration"]
        self.context.comment(f"Current Hold Time: {value}s")
        return int(value)

    def enable(
        self,
        temperature: float | None = None,
        duration: int = 0,
        control_status: ControlStatus = ControlStatus.running,
        control_mode: ControlMode = ControlMode.normal,
    ) -> str:
        """TODO"""
        self.context.comment(
            f"Send "
            f"|Enable Device {temperature}C {duration}s "
            f"{control_status.name} "
            f"{control_mode.normal}| Command"
        )

        if self.simulate:
            return "Enable Device {temperature}C {duration}s {control_status.name} {control_mode.normal}"
        else:
            return self.device.enable()

    def disable(self) -> str:
        """TODO"""
        self.context.comment(f"Send " f"|Disable Device| Command")

        if self.simulate:
            return "Disable Device"
        else:
            return self.device.disable()
