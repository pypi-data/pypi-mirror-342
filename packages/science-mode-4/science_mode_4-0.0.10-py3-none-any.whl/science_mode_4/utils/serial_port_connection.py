"""Provides a class for a serial connection"""

import serial
import serial.tools.list_ports
import serial.tools.list_ports_common

from .connection import Connection
from .logger import logger


class SerialPortConnection(Connection):
    """Serial connection class"""


    @staticmethod
    def list_ports() -> list[serial.tools.list_ports_common.ListPortInfo]:
        """Returns a list of all serial ports"""
        return serial.tools.list_ports.comports()


    @staticmethod
    def list_science_mode_device_ports() -> list[serial.tools.list_ports_common.ListPortInfo]:
        """Returns a list of all serial ports with a science mode device"""
        ports = SerialPortConnection.list_ports()
        # science mode devices (P24/I24) have an STM32 mcu and these are
        # default values for USB CDC devices
        filtered_ports = list(filter(lambda x: x.vid == 0x0483 and x.pid == 0x5740, ports))
        return filtered_ports


    def __init__(self, port: str):
        self._ser = serial.Serial(timeout = 0)
        self._ser.port = port


    def open(self):
        self._ser.open()
        self._ser.set_buffer_size(4096*128)


    def close(self):
        self._ser.close()


    def is_open(self) -> bool:
        return self._ser.is_open


    def write(self, data: bytes):
        self._ser.write(data)


    def read(self) -> bytes:
        result = []
        if self._ser.in_waiting > 0:
            result = self._ser.read_all()
            logger().debug("Incoming data, length: %d, bytes: %s", len(result), result.hex(" ").upper())
        return bytes(result)


    def clear_buffer(self):
        self._ser.reset_input_buffer()
