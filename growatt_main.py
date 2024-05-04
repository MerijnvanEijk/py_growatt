import mqtt_processing
import modbus_processing
import solar_converter_data
import json_reader

import logging

# For sleep
import time


class growatt_runner:
    def __init__(self, path_config):
        self.logger = self.setup_logger()
        self.logger.info("Initializing...")
        self.SolarData = solar_converter_data.solar_converter_data()
        self.logger.info("Gathering data from configuration file...")
        self.JSONData = json_reader.json_reader(path_config)
        self.logger.info("Gathered data from JSON file")

    def setup_logger(self):
        _logger = logging.getLogger("growatt_main")
        logging.basicConfig(
            encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        _logger.debug("Logging start")
        return _logger

    def setup_connections(self):
        self.logger.info("Connecting to MQTT broker...")
        self.mqtt = mqtt_processing.mqtt_processing(
            broker=self.JSONData.host,
            port=self.JSONData.port,
            topic=self.JSONData.topic,
            username=self.JSONData.credentials["username"],
            password=self.JSONData.credentials["password"],
        )
        self.logger.info("Connected to MQTT broker")

        self.logger.info("Opening Serial Modbus...")
        self.modbus = modbus_processing.modbus_processing()
        if self.modbus.connect(port=self.JSONData.device, baudrate=9600) is False:
            self.logger.error("Could not open serial modbus, exiting.")
            self.mqtt.disconnect()
            exit(-1)
        self.logger.info("Opened Serial Modbus")

    def process_frame(self):
        self.logger.info("Reading modbus data")
        address, length = self.SolarData.get_base_register_space(
            self.JSONData.converter
        )
        _modbusData = self.modbus.read_base_registers(address, length)
        if _modbusData is None:
            self.logger.warning("No valid MODBUS Data")
            # Early return nothing left to publish.
            return

        self.SolarData.base_register_conversion(self.JSONData.converter, _modbusData)
        self.logger.info("Publishing data")
        dataList = self.SolarData.get_data_as_list()
        for key, value in dataList:
            self.mqtt.publish(subtopic=key, msg=value)

    def shutdown_connections(self):
        self.mqtt.disconnect()
        self.modbus.disconnect()


runner = growatt_runner("config.json")
runner.setup_connections()
while True:
    runner.process_frame()
    time.sleep(5)

runner.shutdown_connections()
