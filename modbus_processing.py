from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusException
import logging


class modbus_processing:
    def __init__(self):
        self.logger = logging.getLogger("modbus_processing")

    def connect(self, port, baudrate):
        self.client = ModbusSerialClient(port=port, baudrate=baudrate)
        if self.client.connect():
            self.logger.info("Connected to: %s", port)
            return True
        else:
            self.logger.error("Failed to connect to modbus port: %s", port)
            return False

    def disconnect(self):
        self.client.close()

    def read_base_registers(self, addr, length):
        try:
            response = self.client.read_input_registers(addr, length, 1)
            if not response.isError():
                data = [value for value in response.registers]
                return data
            else:
                return None
        except ModbusException as e:
            self.logger.error("Modbus error:", e)
            return None
