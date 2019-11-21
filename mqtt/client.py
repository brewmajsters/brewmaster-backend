import logging
import os
import eventlet
import paho.mqtt.client as mqtt
from paho.mqtt import MQTTException
from core.models import Sensor
from mqtt.mqtt_status import MQTTError

eventlet.monkey_patch()


class MqttClient(object):
    def __init__(self):
        self.app = None
        self.socketio = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = 60
        self.granularity = 5
        self.time = 0

        self.client = mqtt.Client(client_id=os.getenv('MQTT_CLIENT_NAME'))

    def init(self, app, socketio):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.app = app
        self.socketio = socketio

        self.client.on_connect = self.on_connect
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_log(self, clinet, userdata, level, buf):
        logging.getLogger('root_logger').info(f'[MQTT]: Connecting to broker {self.broker_host}: {buf}')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.getLogger('root_logger').info(f'[MQTT]: Successfully connected to broker {self.broker_host}.')
        else:
            raise MQTTException(
                f'[MQTT]: Connection to broker {self.broker_host} refused. Exited with code {MQTTError(rc).name}'
            )

    def on_disconnect(self, client, userdata, flags, rc=0):
        if rc == 0:
            logging.getLogger('root_logger').info(f'[MQTT]: Successfully disconnected from broker {self.broker_host}.')
        else:
            raise MQTTException(
                f'[MQTT]: Disconnection from broker {self.broker_host} refused. Exited with code {MQTTError(rc).name}'
            )

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        string_message = str(msg.payload.decode('utf-8'))
        float_message = float(msg.payload.decode('utf-8'))

        with self.app.app_context():
            self.socketio.emit('new_number',  {'number': float_message}, namespace='/test_web_socket')
            logging.getLogger('root_logger').info(f'[SocketIO]: Sent message: {string_message} to client.')

            if self.time >= self.granularity:
                logging.getLogger('root_logger').info(f'[PostgreSQL]: Created sensor instance: {topic}')
                Sensor(name=topic, message=string_message).create()
                self.time = 0
        self.time += 1
        logging.getLogger('root_logger').info(f'[MQTT]: Message received: {string_message}')

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, name):
        logging.getLogger('root_logger').info(f'[MQTT]: Subscribed to sensor: {name}.')
        self.client.subscribe(name)

    def publish(self, name, message):
        logging.getLogger('root_logger').info(f'[MQTT]: Published message {message} to sensor {name}.')
        self.client.publish(name, message)


mqtt_client = MqttClient()
