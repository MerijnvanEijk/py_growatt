"""Module for conversion from a data array to struct based on converter type for use with modbus"""

import logging
from collections import defaultdict


def single_u16_to_f32(data, factor):
    """Basic conversion function from single U16 to float with factor"""
    return round(float(data) * factor, 3)


def double_u16_to_f32(data1, data2, factor):
    """Basic conversion function from two U16 to float with factor"""
    return round((data1 << 16 | data2) * factor, 3)


class SolarConverterData:
    """Solar Conversion class by converter"""
    def __init__(self):
        self.name = "solar_converter_data"
        self.logger = logging.getLogger(self.name)
        self.data = {
            "status": 0,
            "solarpower": 0,
            "pv1voltage": 0,
            "pv1current": 0,
            "pv1power": 0,
            "pv2voltage": 0,
            "pv2current": 0,
            "pv2power": 0,
            "outputpower": 0,
            "gridfrequency": 0,
            "gridvoltage": 0,
            "energytoday": 0,
            "energytotal": 0,
            "totalworktime": 0,
            "pv1energytoday": 0,
            "pv1energytotal": 0,
            "pv2energytoday": 0,
            "pv2energytotal": 0, 
            "tempinverter": 0,
            "tempipm": 0,
            "tempboost": 0,
        }
        self.converters = {
            "growatt_MIC33xx": {
                "base_registers": self._growatt_MIC_33xx_register_address_space,
                "converion": self._growatt_MIC_33xx_basedata_conversion,
            }
        }

    def reset_data_set(self):
        """Resets the dataset to 0"""
        self.data = {
            "status": 0,
            "solarpower": 0,
            "pv1voltage": 0,
            "pv1current": 0,
            "pv1power": 0,
            "pv2voltage": 0,
            "pv2current": 0,
            "pv2power": 0,
            "outputpower": 0,
            "gridfrequency": 0,
            "gridvoltage": 0,
            "energytoday": 0,
            "energytotal": 0,
            "totalworktime": 0,
            "pv1energytoday": 0,
            "pv1energytotal": 0,
            "pv2energytoday": 0,
            "pv2energytotal": 0, 
            "tempinverter": 0,
            "tempipm": 0,
            "tempboost": 0,
        }

    def print_data(self):
        """Debug printing from dict for stored values."""
        self.logger.info("Current %s: %s", self.name, self.data)

    def get_data_as_string(self):
        """Returns data as full string set for printing."""
        return "\n".join("%s: %s" % (key, value) for key, value in self.data.items())

    def get_data_as_list(self):
        """Returns List of data set stored with values"""
        return list(self.data.items())

    def get_base_register_space(self, type):
        """Gets length of addresses to request by modbus based on type."""
        return self.converters[type]["base_registers"]()

    def base_register_conversion(self, type, array_data):
        """Converts array_data from a modbus request stored in the class."""
        return self.converters[type]["converion"](array_data)

    # privates
    # Unique conversion per supported type.
    def _growatt_MIC_33xx_register_address_space(self):
        """MIC33xx Length of register space for modbus."""
        return 0, 96

    def _growatt_MIC_33xx_basedata_conversion(self, array_data):
        """MIC33xx Conversion to struct from data array"""
        self.data = {
            "status": single_u16_to_f32(array_data[0], 1.0),
            "solarpower": double_u16_to_f32(array_data[1], array_data[2], 0.1),
            "pv1voltage": single_u16_to_f32(array_data[3], 0.1),
            "pv1current": single_u16_to_f32(array_data[4], 0.1),
            "pv1power": double_u16_to_f32(array_data[5], array_data[6], 0.1),
            "pv2voltage": single_u16_to_f32(array_data[7], 0.1),
            "pv2current": single_u16_to_f32(array_data[8], 0.1),
            "pv2power": double_u16_to_f32(array_data[9], array_data[10], 0.1),
            "outputpower": double_u16_to_f32(array_data[35], array_data[36], 0.1),
            "gridfrequency": single_u16_to_f32(array_data[37], 0.01),
            "gridvoltage": single_u16_to_f32(array_data[38], 0.1),
            "energytoday": double_u16_to_f32(array_data[53], array_data[54], 0.1),
            "energytotal": double_u16_to_f32(array_data[55], array_data[56], 0.1),
            "totalworktime": double_u16_to_f32(array_data[57], array_data[58], 0.5),
            "pv1energytoday": double_u16_to_f32(array_data[59], array_data[60], 0.1),
            "pv1energytotal": double_u16_to_f32(array_data[61], array_data[62], 0.1),
            "pv2energytoday": double_u16_to_f32(array_data[63], array_data[64], 0.1),
            "pv2energytotal": double_u16_to_f32(array_data[65], array_data[66], 0.1),
            "tempinverter": single_u16_to_f32(array_data[93], 0.1),
            "tempipm": single_u16_to_f32(array_data[94], 0.1),
            "tempboost": single_u16_to_f32(array_data[95], 0.1),
        }
