import json
import logging
import os
import eventlet
import paho.mqtt.client as mqtt
from core.models import Sensor, Module
from mqtt import mqtt_status
from mqtt.errors import MQTTException

eventlet.monkey_patch()


class MqttClient(object):
    def __init__(self):
        self.app = None
        self.socketio = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = 60
        self.granularity = 5
        self.time = {}

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
                f'[MQTT]: Connection to broker {self.broker_host} refused.',
                status_code=mqtt_status.MQTT_ERR_CONN_REFUSED
            )

    def on_disconnect(self, client, userdata, flags, rc=0):
        if rc == 0:
            logging.getLogger('root_logger').info(f'[MQTT]: Successfully disconnected from broker {self.broker_host}.')
        else:
            raise MQTTException(
                f'[MQTT]: Disconnection from broker {self.broker_host} refused.',
                status_code=mqtt_status.MQTT_ERR_CONN_LOST
            )

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        string_message = str(msg.payload.decode('utf-8'))

        with self.app.app_context():
            module = Module.query.filter_by(mac=topic).first()

            # Received from module
            if module:
                dict_message = json.loads(string_message)

                if dict_message.get('result') == 'OK':
                    logging.getLogger('root_logger').info(f'[MQTT]: Message received: {string_message}')
                elif dict_message.get('result') == 'ERROR':
                    raise MQTTException(dict_message.get('details'), status_code=mqtt_status.MQTT_ERR_NOT_SUPPORTED)
                else:
                    logging.getLogger('root_logger').info(f'[MQTT]: Message received: {string_message}')

            # Received from sensor
            else:
                float_message = float(msg.payload.decode('utf-8'))

                self.socketio.emit(topic, {'number': float_message}, namespace='/test_web_socket')
                logging.getLogger('root_logger').info(f'[SocketIO]: Sent message: {string_message} to client.')

                if not topic in self.time:
                    self.time[topic] = 0

                if self.time.get(topic) >= self.granularity:
                    logging.getLogger('root_logger').info(f'[PostgreSQL]: Created sensor instance: {topic}')
                    Sensor(name=topic, message=string_message).create()
                    self.time[topic] = 0

                self.time[topic] += 1
                logging.getLogger('root_logger').info(f'[MQTT]: Message received: {string_message}')

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, name):
        logging.getLogger('root_logger').info(f'[MQTT]: Subscribed to device: {name}.')
        self.client.subscribe(name)

    def publish(self, name, message):
        logging.getLogger('root_logger').info(f'[MQTT]: Published message {message} to sensor {name}.')
        self.client.publish(name, message)


mqtt_client = MqttClient()
