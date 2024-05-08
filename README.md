# PY Growatt
This is a small python script that reads out growatt solar converter via modbus and posts it to an MQTT broker.
It will push every 5 seconds the data set to the MQTT server. Information to support it in homeassistant is described in the integration section.

This repo is inspired by: https://github.com/nygma2004/growatt2mqtt/tree/main , but for RPi or other PC linux based devices.
I used it to cross-reference the minimal register interface also mentioned in the growatt modbus registery datasheet.

## Future improvements/validations TODO's:
- Support more (Growatt) converters (modbus)
- Support more mqtt server connection options (no credentials/TLS'ed)
- Support error registers of growatt

## Requirements Hardware
- A Raspberry PI or PC running linux.
- (MODBUS/RS485) serial converter. Like a CH340.

## Requirements Software
Python (3.11) Requirements.txt, you can use a python venv to run it, or install the requirements.txt

## Configuration
In the Config.json you can setup the device(serial port) and mqtt broker. Currently only credential support is added.
Currently only a Growatt MIC33xx or probably the 3x / 2x series are supported via MODBUS.(Other than MIC 33xx are untested)

## Startup
Clone this repo
`git clone https://github.com/MerijnvanEijk/py_growatt.git`
Modify the configuration if needed.
Execute to run the script.
`python3 growatt_main.py` 
If you want to run it continously, you can run it in a screen and use:
`python3 growatt_main.py&` 

## Home assistant integration.
If you want to link it to home assistant the following mqtt devices should be added. (If you left the topics the same)
These are the basic sensors and are compatible with the energy dashboard(Home-assistant core version 2024.4.4)
```YAML
mqtt:
 sensor:
 - name: "PV_current_power"
   state_topic: "growatt/reading/outputpower"
   unit_of_measurement: "W"
   device_class: "power"
   state_class: "measurement"
 - name: "PV_total_daily_power"
   state_topic: "growatt/reading/energytoday"
   unit_of_measurement: "kWh"
   device_class: "energy"
   state_class: "total_increasing"
 - name: "PV_total_power"
   state_topic: "growatt/reading/energytotal"
   unit_of_measurement: "kWh"
   device_class: "energy"
   state_class: "total"
 - name: "PV_temperature"
   state_topic: "growatt/reading/tempinverter"
   unit_of_measurement: "°C"
   device_class: "temperature"
   state_class: "measurement"
 - name: "PV_voltage"
   state_topic: "growatt/reading/pv1voltage"
   unit_of_measurement: "V"
   device_class: "voltage"
   state_class: "measurement"
 - name: "PV_grid_voltage"
   state_topic: "growatt/reading/gridvoltage"
   unit_of_measurement: "V"
   device_class: "voltage"
   state_class: "measurement"
 - name: "PV_grid_frequency"
   state_topic: "growatt/reading/gridfrequency"
   unit_of_measurement: "Hz"
   device_class: "frequency"
   state_class: "measurement"
```

