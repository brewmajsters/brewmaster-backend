import json
import logging
import os
import time
import eventlet
import paho.mqtt.client as mqtt
from core.models import Module, ModuleNotification
from mqtt import mqtt_status
from mqtt.errors import MQTTException

eventlet.monkey_patch()


class MqttClient(object):
    def __init__(self):
        self.app = None
        self.socketio = None
        self.broker_host = None
        self.broker_port = None
        self.keep_alive = None
        self.timeout = None
        self.db_blocker = []
        self.ack_blocker = []

        self.client = mqtt.Client(client_id=os.getenv('MQTT_CLIENT_NAME'))

    def init(self, app, socketio):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.keep_alive = int(os.getenv('MQTT_KEEPALIVE'))
        self.timeout = int(os.getenv('MQTT_TIMEOUT'))
        self.app = app
        self.socketio = socketio

        self.client.on_connect = self.on_connect
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def start_mqtt_connections(self):
        modules = Module.query.all()

        for module in modules:
            mqtt_client.subscribe(module.mac)

            # TODO: Nastavit granularitu ukladania zaznamov do DB
            self.db_blocker.append({
                'module_mac': module.mac,
                'granularity': 10,
                'time': 0
            })

            self.ack_blocker.append({
                'module_mac': module.mac,
                'blocked': False,
                'message': None
            })

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
        dict_message = json.loads(string_message)

        with self.app.app_context():
            module = Module.query.filter_by(mac=topic).first()

            if not module:
                raise MQTTException(
                    f'Špecifikovaný modul s mac nebol nájdený: {topic}',
                    status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                )

            # Request result
            if dict_message.get('result'):
                module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == topic, self.ack_blocker), None)
                module_ack_blocker['blocked'] = False
                module_ack_blocker['message'] = dict_message

            # Value update asynchronously
            elif dict_message.get('values'):
                values = dict_message.get('values')

                for key, value in values.items():
                    device = module.devices.filter_by(id=key)

                    if not device:
                        raise MQTTException(
                            f'Špecifikovaný device nebol nájdený: {key}',
                            status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                        )

                    self.socketio.emit(topic, dict_message, namespace='/web_socket')
                    logging.getLogger('root_logger').info(f'[SocketIO]: Posielaná správa: {string_message} na webový klient.')

                module_db_blocker = next(filter(lambda obj: obj.get('module_mac') == topic, self.db_blocker), None)

                if module_db_blocker.get('time') >= module_db_blocker.get('granularity'):
                    logging.getLogger('root_logger').info(
                        f'[PostgreSQL]: Vytvorená inštancia v histórii posielaných dát: {topic}'
                    )
                    ModuleNotification(module=module, message=json.dumps(values)).create()
                    module_db_blocker['time'] = 0

                module_db_blocker['time'] += 1

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

    def publish(self, mac, message):
        logging.getLogger('root_logger').info(f'[MQTT]: Published message {message} to modul {mac}.')
        module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)
        module_ack_blocker['blocked'] = True
        module_ack_blocker['message'] = None
        self.client.publish(mac, message)

    def get_ack_block(self, mac):
        module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)
        return module_ack_blocker.get('blocked')

    def get_ack_message(self, mac):
        module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)
        return module_ack_blocker.get('message')

    def send_message(self, mac: str, message: str):
        self.publish(mac, message)

        end_time = time.time() + self.timeout

        while True:
            module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)

            if not module_ack_blocker.get('blocked'):
                response = module_ack_blocker.get('message')

                if response.get('result') == 'OK':
                    logging.getLogger('root_logger').info(f'[MQTT]: ACK Message received.')
                    return response
                elif response.get('result') == 'ERROR':
                    raise MQTTException(response.get('details'), status_code=mqtt_status.MQTT_ERR_NOT_SUPPORTED)

            if time.time() < end_time:
                return MQTTException('Daný modul neodpovedá.', status_code=mqtt_status.MQTT_ERR_UNKNOWN)


mqtt_client = MqttClient()
