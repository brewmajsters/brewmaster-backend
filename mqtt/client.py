import logging
import os
import paho.mqtt.client as mqtt
from paho.mqtt import MQTTException
from core.models import Sensor
from mqtt.mqtt_status import MQTTError


class MqttClient(object):
    def __init__(self):
        self.app = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = 60

        self.client = mqtt.Client(client_id=os.getenv('MQTT_CLIENT_NAME'))

    def init(self, app):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.app = app

        self.client.on_connect = self.on_connect
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_log(self, clinet, userdata, level, buf):
        logging.getLogger('root_logger').info(f'Connecting to broker {self.broker_host}: {buf}')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.getLogger('root_logger').info(f'Successfully connected to broker {self.broker_host}.')
        else:
            raise MQTTException(
                f'Connection to broker {self.broker_host} refused. Exited with code {MQTTError(rc).name}'
            )

    def on_disconnect(self, client, userdata, flags, rc=0):
        if rc == 0:
            logging.getLogger('root_logger').info(f'Successfully disconnected from broker {self.broker_host}.')
        else:
            raise MQTTException(
                f'Disconnection from broker {self.broker_host} refused. Exited with code {MQTTError(rc).name}'
            )

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode('utf-8'))

        with self.app.app_context():
            Sensor(name=topic, message=m_decode).create()
        logging.getLogger('root_logger').info(f'Message received: {m_decode}')

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, name):
        self.client.subscribe(name)

    def publish(self, name, message):
        self.client.publish(name, message)


mqtt_client = MqttClient()
