import json
import logging
from random import random
from threading import Thread, Event
from core.models import Module
from mqtt.client import mqtt_client


class Sensor(object):
    def __init__(self, name, socket_io):
        self.thread = Thread()
        self.thread_stop_event = Event()
        self.name = name
        self.socket_io = socket_io

    def run(self):
        if not self.thread.is_alive():
            thread = RandomThread(self.name, self.socket_io, self.thread_stop_event)
            thread.start()
            logging.getLogger('root_logger').info(f'[Sensor {self.name}]: Thread started.')

    def stop(self):
        if self.thread.isAlive():
            self.thread_stop_event.set()
        logging.getLogger('root_logger').info(f'[Sensor {self.name}]: Thread ended.')


class RandomThread(Thread):
    def __init__(self, name, socket_io, thread_stop_event):
        self.thread_stop_event = thread_stop_event
        self.socket_io = socket_io
        self.sensor_name = name
        self.delay = 1
        super(RandomThread, self).__init__()

    def run(self):
        while not self.thread_stop_event.isSet():
            data = {
                "module_mac": self.sensor_name,
                "values": {},
            }

            with self.socket_io.sockio_mw.flask_app.app_context():
                module = Module.query.filter_by(mac=self.sensor_name).first()
                devices = module.devices

                for device in devices:
                    data['values'][str(device.id)] = {
                        'value': round(random() * 10, 3),
                        'unit': 'value',
                        'writable': True
                    }

            mqtt_client.publish(self.sensor_name, json.dumps(data))
            self.socket_io.sleep(self.delay)
