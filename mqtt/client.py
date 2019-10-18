import logging
import os
import paho.mqtt.client as mqtt


class MqttClient(object):
    def __init__(self):
        self.broker_host = os.getenv('BROKER_HOST')
        self.broker_port = int(os.getenv('BROKER_PORT'))
        self.keep_alive = 60

        self.client = mqtt.Client('brewmaster_client')
        self.client.on_connect = self.on_connect
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_log(self, clinet, userdata, level, buf):
        logging.info(f'Connecting to broker {self.broker_host}: {buf}')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f'Successfully connected to broker {self.broker_host}.')
        else:
            logging.error(f'Connection to broker {self.broker_host} refused. RC: {rc}')

    def on_disconnect(self, client, userdata, flags, rc=0):
        if rc == 0:
            logging.info(f'Successfully disconnected from broker {self.broker_host}.')
        else:
            logging.error(f'Disconnection from broker {self.broker_host} refused. RC: {rc}')

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode('utf-8'))
        logging.info(f'Message received: {m_decode}')

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
