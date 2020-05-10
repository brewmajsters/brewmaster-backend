import json
import os
import paho.mqtt.client as mqtt
from core.models import Module
from mqtt.emulator.module_emulator import ModuleEmulator


class MqttClientEmulator(object):
    def __init__(self):
        self.app = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = None
        self.timeout = None
        self.module_emulators = []

        self.client = mqtt.Client(client_id='brewmaster_client_emulator')

    def init(self, app):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.keep_alive = int(os.getenv('MQTT_KEEPALIVE'))
        self.timeout = int(os.getenv('MQTT_TIMEOUT'))
        self.app = app

        self.client.on_message = self.on_message

    def generate_modules(self):
        for module in Module.query.all():
            module_emulator = ModuleEmulator(module.mac, self.app, self)
            self.module_emulators.append(module_emulator)
            module_emulator.run()

    def _handle_set_module_value(self, mac, data):
        module = None

        for module_emulator in self.module_emulators:
            if module_emulator.mac == mac:
                module = module_emulator

        if module:
            module.set_value(data)

            response = {
                "module_mac": mac,
                "sequence_number": 123,
                "result": "OK",
                "details": ""
            }
        else:
            response = {
                "module_mac": mac,
                "sequence_number": 123,
                "result": "ERROR",
                "details": "Module does not exist!!!"
            }
        self.publish('REQUEST_RESULT', json.dumps(response))

    def _handle_set_module_config(self, mac, data):
        module = None

        for module_emulator in self.module_emulators:
            if module_emulator.mac == mac:
                module = module_emulator

        if module:
            module.set_config(data)

            response = {
                "module_mac": mac,
                "sequence_number": 123,
                "result": "OK",
                "details": ""
            }
        else:
            response = {
                "module_mac": mac,
                "sequence_number": 123,
                "result": "ERROR",
                "details": "Module does not exist!!!"
            }
        self.publish('REQUEST_RESULT', json.dumps(response))

    def on_message(self, client, userdata, msg):
        topic = msg.topic

        if '/' in topic:
            mac = topic.split('/')[0]
        else:
            mac = None

        string_message = str(msg.payload.decode('utf-8'))
        dict_message = json.loads(string_message)

        # Request result
        if 'SET_VALUE' in topic:
            self._handle_set_module_value(mac, dict_message)
        elif 'SET_CONFIG' in topic:
            self._handle_set_module_config(mac, dict_message)

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
