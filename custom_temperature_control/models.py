""""todo"."""

import sys
from enum import Enum

TargetDevicePid: int = 29987


class CommandCode(Enum):
    """TODO"""

    GET_VERSION = "01"
    RESTART = "02"
    GET_STATUS = "03"
    ENABLE = "04"
    DISABLE = "05"
    CALIBRATE = "10"


class ResponseCode(Enum):
    """TODO"""

    GET_VERSION = "A1"
    RESTART = "A2"
    GET_STATUS = "A3"
    ENABLE = "A4"
    DISABLE = "A5"
    CALIBRATE = "B5"

    @classmethod
    def get_map(cls, target: str) -> str:
        """todo"""
        response = cls._member_map_.get(target)
        assert response is not None
        return str(response.value)  # type ignore[union-attr]


class ControlStatus(Enum):
    """todo"""

    running: int = 0x01
    stopped: int = 0x00

    @classmethod
    def get_status(cls, target: int) -> "ControlStatus":
        """todo"""
        value = target & 0x01
        if value == cls.running.value:
            return cls.running
        elif value == cls.stopped.value:
            return cls.stopped
        else:
            raise ValueError("当前状态不可识别")


class ControlMode(Enum):
    """todo"""

    normal: int = 0x00
    calibrate: int = 0x80

    @classmethod
    def get_mode(cls, target: int) -> "ControlMode":
        """todo"""
        value = target & 0x80
        if value == cls.normal.value:
            return cls.normal
        elif value == cls.calibrate.value:
            return cls.calibrate
        else:
            raise ValueError("当前模式不可识别")


class ErrorCode(Enum):
    """todo"""

    normal: int = 0x00
    offline: int = 0x01
    breakdown: int = 0x02

    @classmethod
    def get_value(cls, target: int) -> "ErrorCode":
        """todo"""
        value = target & 0x03
        if value == cls.normal.value:
            return cls.normal
        elif value == cls.offline.value:
            return cls.offline
        elif value == cls.breakdown.value:
            return cls.breakdown
        else:
            raise ValueError("当前异常不可识别")


class RunStatus(Enum):
    """todo"""

    running: int = 0x01
    idle: int = 0x00

    @classmethod
    def get_value(cls, target: int) -> "RunStatus":
        """todo"""
        value = target & 0x01
        if value == cls.running.value:
            return cls.running
        elif value == cls.idle.value:
            return cls.idle
        else:
            raise ValueError("当前状态不可识别")
