""""todo"."""

from enum import Enum


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
