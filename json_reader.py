"""Modyle to read growatt_py json configs."""
import logging
import json


class JsonReader:
    """JSON reader class"""
    def __init__(self, path):
        self.logger = logging.getLogger("json_reader")
        self.open(path)

    def open(self, path):
        """Opens (JSON config) file for reading, parses it and closes it"""
        self.logger.info("Opening %s", path)
        retval = None
        with open(path, encoding="utf-8") as file:
            self.data = json.load(file)
            retval = self.parse()
            file.close()

        return retval

    def parse(self):
        """Parses JSON file"""
        # Keep this as a function for future sanity checking.
        self.device = self.data["device"]
        self.topic = self.data["topic"]
        self.host = self.data["host"]
        self.port = self.data["port"]
        self.converter = self.data["converter"]
        self.credentials = self.data["credentials"]
        self.logger.debug(self.device)
        self.logger.debug(self.host)
        self.logger.debug(self.port)
        self.logger.debug(self.credentials)
        return True
