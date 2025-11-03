"""Main function entry, mainly used for debugging."""

import logging

from art_dam_3254.driver import BaseDriver
from art_dam_3254.models import AnalogChannel, SwitchStatus, DigitalOutputMode

logging.basicConfig(
    level=logging.DEBUG,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

if __name__ == "__main__":

    swr = BaseDriver(port="/dev/ttyUSB0",baud_rate=9600,timeout=5,device_address="01")
    swr.connect()

    res = swr.get_analog_channel_value(AnalogChannel.ch1)
    print(res)

    res = swr.get_analog_channel_value(AnalogChannel.ch2)
    print(res)

    res = swr.get_analog_channel_value(AnalogChannel.ch3)
    print(res)

    res = swr.get_analog_channel_value(AnalogChannel.ch4)
    print(res)

    res = swr.get_all_analog_channel_value()
    print(res)

    res = swr.get_digital_input_1_work_mode()
    print(res)

    res = swr.get_analog_channel_range(AnalogChannel.ch1)
    print(res)

    res = swr.get_digital_input_1_status()
    print(res)

    res = swr.set_digital_output_1_status(SwitchStatus.Off,DigitalOutputMode.Engage)

    swr.disconnect()