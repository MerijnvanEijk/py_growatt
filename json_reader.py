import logging
import json


class json_reader:
    def __init__(self, path):
        self.logger = logging.getLogger("json_reader")
        self.open(path)

    def open(self, path):
        self.logger.info("Opening %s", path)
        file = open(path)
        self.data = json.load(file)
        retval = self.parse()
        file.close
        return retval

    def parse(self):
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
