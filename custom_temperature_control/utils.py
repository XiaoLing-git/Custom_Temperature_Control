""""todo"."""

import logging

logger = logging.getLogger(__name__)


def assert_hex_code(target: str) -> None:
    """
    assert target is hex code,
    :param target:
    :return:
    """
    if len(target) == 0:
        return
    for c in target:
        if c.upper() not in "0123456789ABCDEF":
            raise ValueError(f"char {c} can't not hex()")
    return


def modbus_crc16(target: str) -> str:
    """Calculate modbus crc code."""
    target = target.replace(" ", "")
    if len(target) == 0:
        raise ValueError("length target data is 0")

    try:
        result = 0
        for item in [target[i : i + 2] for i in range(0, len(target), 2)]:
            res = int.from_bytes(bytes.fromhex(item), byteorder="big")
            result = result ^ res
        re_result = int.to_bytes(result, byteorder="big", length=1).hex()
    except Exception as e:
        raise ValueError(f"An exception occurred during calculation: {e}")
    logger.debug(f"Crc16 Target: {target.upper()} Result: {re_result.upper()}")
    return re_result.upper()
