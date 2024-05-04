from paho.mqtt import client as mqtt_client
import random
import logging
import time

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


class mqtt_processing:
    def __init__(
        self, broker, port, topic="growatt/reading", username=None, password=None
    ):
        self.logger = logging.getLogger("mqtt_processing")
        self.logger.info("MQTT local init")
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.connect()

    def connect(self):
        self.logger.info("MQTT local connect")
        client_id = "python-mqtt-" + str(random.randint(0, 1000))
        client = mqtt_client.Client(
            client_id=client_id,
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
        )
        client.on_connect = self.on_connect  # Callback on connect
        client.on_disconnect = self.on_disconnect  # Callback on connect
        client.username_pw_set(self.username, self.password)
        client.connect(self.broker, self.port)

        self.client = client

    def on_connect(self, userdata, flags, rc, properties):
        if rc == 0:
            self.logger.info("Connected to MQTT Broker!")
        else:
            self.logger.error("Failed to connect, return code %d\n", rc)

    def on_disconnect(
        self, client, not_available, disconnect_flags, reason_code, properties
    ):
        self.logger.info("Disconnected with result code: %s", reason_code)
        if reason_code.getName() == "Normal disconnection":
            self.logger.info("Disconnect from client side")
            return

        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            self.logger.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                self.logger.info("Reconnected successfully!")
                return
            except Exception as err:
                self.logger.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1

        self.logger.info(
            "Reconnect failed after %s attempts. Exiting...", reconnect_count
        )

    def publish(self, msg, subtopic=None):
        if subtopic:
            _topic = self.topic + "/" + subtopic
        else:
            _topic = self.topic

        result = self.client.publish(_topic, msg)
        status = result[0]
        if status == 0:
            self.logger.info("Send %s to topic %s", msg, _topic)
            return 0
        else:
            self.logger.warning("Failed to send message to topic %s", _topic)
            return -1

    def disconnect(self):
        self.client.disconnect()
