import json
import logging
import os
import time
import eventlet
import paho.mqtt.client as mqtt
from core.models import Module, ModuleNotification, Measurement, DeviceDatapoint
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
        self.subscribed_topics = [
            'MODULE_ID', 'MODULE_DISCONNECT', 'MODULE_CONFIG_UPDATE', 'VALUE_UPDATE', 'REQUEST_RESULT'
        ]
        self.published_topics = [
            'REQUEST', 'UPDATE_FW', 'SET_VALUE', 'SET_CONFIG', 'ALL_MODULES'
        ]

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
        for topic in self.subscribed_topics:
            mqtt_client.subscribe(topic)

        modules = Module.query.all()

        for module in modules:
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

    def _handle_periodical_value_reports(self, data):
        with self.app.app_context():
            module_mac = data.get('module_mac')
            values = data.get('values')

            module = Module.query.filter_by(mac=module_mac).first()

            if not module:
                raise MQTTException(
                    f'Špecifikovaný modul s mac nebol nájdený: {module_mac}',
                    status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                )

            for key, value in values.items():
                device = module.devices.filter_by(id=key)

                if not device:
                    raise MQTTException(
                        f'Špecifikovaný device nebol nájdený: {key}',
                        status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                    )

                for datapiont_code, datapoint_value in values:
                    datapoint = DeviceDatapoint.query.filter_by({'device_id': device.id, 'code':datapiont_code}).first()
                    if not datapoint:
                        raise MQTTException(
                            f'Špecifikovaný datapoint nebol nájdený: {key}',
                            status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                        )
                    Measurement(datapoint=datapoint, value=datapoint_value)

                self.socketio.emit(str(module.id), data, namespace='/web_socket')
                logging.getLogger('root_logger').info(f'[SocketIO]: Posielaná správa: {data} na webový klient.')

            module_db_blocker = next(filter(lambda obj: obj.get('module_mac') == module_mac, self.db_blocker), None)

            if module_db_blocker.get('time') >= module_db_blocker.get('granularity'):
                logging.getLogger('root_logger').info(
                    f'[PostgreSQL]: Vytvorená inštancia v histórii posielaných dát: {module_mac}'
                )
                ModuleNotification(module=module, message=json.dumps(values)).create()
                module_db_blocker['time'] = 0

            module_db_blocker['time'] += 1

    def _handle_result_reports(self, data):
        with self.app.app_context():
            module_mac = data.get('module_mac')

            module = Module.query.filter_by(mac=module_mac).first()

            if not module:
                raise MQTTException(
                    f'Špecifikovaný modul s mac nebol nájdený: {module_mac}',
                    status_code=mqtt_status.MQTT_ERR_NOT_FOUND
                )

            module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == module_mac, self.ack_blocker), None)
            module_ack_blocker['blocked'] = False
            module_ack_blocker['message'] = data

    def _handle_module_config_update(self, data):
        pass

    def _handle_module_discovery(self, data):
        pass

    def _handle_module_disconnect(self, data):
        pass

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

        # Request result
        if topic == 'REQUEST_RESULT':
            self._handle_result_reports(dict_message)

        # Value update asynchronously
        elif topic == 'VALUE_UPDATE':
            self._handle_periodical_value_reports(dict_message)

        elif topic == 'MODULE_CONFIG_UPDATE':
            self._handle_module_config_update(dict_message)

        elif topic == 'MODULE_ID':
            self._handle_module_discovery(dict_message)

        elif topic == 'MODULE_DISCONNECT':
            self._handle_module_disconnect(dict_message)

        logging.getLogger('root_logger').info(f'[MQTT]: Message received: {string_message}')

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, name):
        logging.getLogger('root_logger').info(f'[MQTT]: Subscribed to topic: {name}.')
        self.client.subscribe(name)

    def publish(self, mac, topic, message):
        logging.getLogger('root_logger').info(f'[MQTT]: Published message {message} to topic {topic}.')
        module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)
        module_ack_blocker['blocked'] = True
        module_ack_blocker['message'] = None
        return self.client.publish(topic, message)

    def send_message(self, mac: str, topic: str, message: str):
        if topic in self.published_topics:
            topic = f'{mac}/{topic}' if mac else topic
        else:
            raise MQTTException(
                'Daný topic nie je medzi povolenými topicmi.', status_code=mqtt_status.MQTT_ERR_NOT_FOUND
            )

        result = self.publish(mac, topic, message)
        end_time = time.time() + self.timeout

        if result.rc == mqtt.MQTT_ERR_QUEUE_SIZE:
            raise ValueError('Message is not queued due to ERR_QUEUE_SIZE')
        with result._condition:
            while True:
                module_ack_blocker = next(filter(lambda obj: obj.get('module_mac') == mac, self.ack_blocker), None)

                if not module_ack_blocker.get('blocked'):
                    response = module_ack_blocker.get('message')

                    if response.get('result') == 'OK':
                        logging.getLogger('root_logger').info(f'[MQTT]: ACK Message received.')
                        return response
                    elif response.get('result') == 'ERROR':
                        raise MQTTException(response.get('details'), status_code=mqtt_status.MQTT_ERR_NOT_SUPPORTED)

                if time.time() > end_time:
                    raise MQTTException('Daný modul neodpovedá.', status_code=mqtt_status.MQTT_ERR_UNKNOWN)
                result._condition.wait(1)


mqtt_client = MqttClient()
