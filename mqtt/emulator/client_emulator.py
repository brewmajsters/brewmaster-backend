import json
import os
import time
import paho.mqtt.client as mqtt


class MqttClientEmulator(object):
    def __init__(self):
        self.app = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = None
        self.timeout = None

        self.client = mqtt.Client(client_id='brewmaster_client_emulator')

    def init(self, app):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.keep_alive = int(os.getenv('MQTT_KEEPALIVE'))
        self.timeout = int(os.getenv('MQTT_TIMEOUT'))
        self.app = app

        self.client.on_message = self.on_message

    def _handle_ack_result(self, topic):
        response = {
            "module_mac": topic,
            "sequence_number": 123,
            "result": "OK",
            "details": ""
        }
        time.sleep(1)   # Just for time reserve (this code will be more complicated in future)
        self.publish('brewmaster-backend', json.dumps(response))

    def _handle_err_result(self, topic):
        response = {
            "module_mac": topic,
            "sequence_number": 123,
            "result": "ERROR",
            "details": "Some unexpected error occurred"
        }
        time.sleep(1)   # Just for time reserve (this code will be more complicated in future)
        self.publish('brewmaster-backend', json.dumps(response))

    def _handle_no_result(self, topic):
        time.sleep(20)
        response = {
            "module_mac": topic,
            "sequence_number": 123,
            "result": "OK",
            "details": ""
        }
        self.publish('brewmaster-backend', json.dumps(response))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        string_message = str(msg.payload.decode('utf-8'))
        dict_message = json.loads(string_message)

        # Request result
        if dict_message.get('device_uuid'):
            self._handle_ack_result(topic)

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, name):
        self.client.subscribe(name)

    def publish(self, topic, message):
        self.client.publish(topic, message)


mqtt_client_emulator = MqttClientEmulator()
