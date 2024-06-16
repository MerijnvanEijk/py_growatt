"""Module for handling basic modbus functionality."""
import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusException


class ModbusProcessing:
    """Class to handle basic Modbus interpretations"""
    def __init__(self,port, baudrate):
        self.logger = logging.getLogger("modbus_processing")
        self.port = port
        self.baudrate = baudrate
        self.client = ModbusSerialClient(port=port, baudrate=baudrate)

    def connect(self):
        """Connect to Modbus based on port and baudrate"""
        if self.client.connect():
            self.logger.info("Connected to: %s", self.port)
            return True
        else:
            self.logger.error("Failed to connect to modbus port: %s", self.port)
            return False

    def disconnect(self):
        """Disconnect to Modbus based"""
        self.client.close()

    def read_base_registers(self, addr, length):
        """Read a set of base registers based on starting address and length"""
        try:
            response = self.client.read_input_registers(addr, length, 1)
            if not response.isError():
                data = [value for value in response.registers]
                return data
            else:
                return None
        except ModbusException as e:
            self.logger.error("Modbus error: %s", e)
            return None
