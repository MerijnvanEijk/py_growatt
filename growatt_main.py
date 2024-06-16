"""Growatt Reader Main entry class and execution loop"""
import logging
# For sleep
import time
import mqtt_processing
import modbus_processing
import solar_converter_data
import json_reader


class GrowattRunner:
    """Growatt operating class."""
    def __init__(self, path_config):
        self.logger = self.setup_logger()
        self.logger.info("Initializing...")
        self.SolarData = solar_converter_data.SolarConverterData()
        self.logger.info("Gathering data from configuration file...")
        self.JSONData = json_reader.JsonReader(path_config)
        self.logger.info("Gathered data from JSON file")

    def setup_logger(self):
        """Setup loggers for reporting and debugging"""
        _logger = logging.getLogger("growatt_main")
        logging.basicConfig(
            encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        _logger.debug("Logging start")
        return _logger

    def setup_connections(self):
        """Should be called once to setup connections to MQTT broker and the modbus port"""
        self.logger.info("Connecting to MQTT broker...")
        # MQTT section
        self.mqtt = mqtt_processing.MQTTProcessing(
            broker=self.JSONData.host,
            port=self.JSONData.port,
            topic=self.JSONData.topic,
            username=self.JSONData.credentials["username"],
            password=self.JSONData.credentials["password"],
        )
        self.logger.info("Connected to MQTT broker")
        # MODBUS section
        self.logger.info("Opening Serial Modbus...")
        self.modbus = modbus_processing.ModbusProcessing(port=self.JSONData.device, baudrate=9600)
        if self.modbus.connect() is False:
            self.logger.error("Could not open serial modbus, exiting.")
            self.mqtt.disconnect()
            exit(-1)
        self.logger.info("Opened Serial Modbus")

    def process_frame(self):
        """Should be called iteratively to request MODBUS frame and send it to the broker"""
        self.logger.info("Reading modbus data")
        address, length = self.SolarData.get_base_register_space(
            self.JSONData.converter
        )
        _modbusData = self.modbus.read_base_registers(address, length)
        if _modbusData is None:
            # Resetting data set to 0, to ensure it gets logged correctly.
            # Also every night the convertors are disconnected, for Home-assistant 
            # it defaults to this value.
            self.logger.warning("No valid MODBUS Data")
            self.SolarData.reset_data_set()

        self.SolarData.base_register_conversion(self.JSONData.converter, _modbusData)
        self.logger.info("Publishing data")
        dataList = self.SolarData.get_data_as_list()
        for key, value in dataList:
            self.mqtt.publish(subtopic=key, msg=value)

    def shutdown_connections(self):
        self.mqtt.disconnect()
        self.modbus.disconnect()


runner = GrowattRunner("config.json")
runner.setup_connections()
while True:
    runner.process_frame()
    time.sleep(5)

runner.shutdown_connections()
