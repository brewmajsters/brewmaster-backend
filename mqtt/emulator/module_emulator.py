import json
import logging
import random
import time
from threading import Thread, Event
from core.models import Module


class ModuleEmulator(object):
    def __init__(self, name, app, mqtt_client):
        self.mqtt_client = mqtt_client
        self.thread = Thread()
        self.thread_stop_event = Event()
        self.name = name
        self.app = app
        self.module_thread = None

    def run(self):
        if not self.thread.is_alive():
            self.module_thread = RandomThread(self.name, self.app, self.thread_stop_event, self.mqtt_client)
            self.module_thread.start()
            logging.getLogger('root_logger').info(f'[EMULATOR {self.name}]: Thread started.')

    def stop(self):
        if self.thread.isAlive():
            self.thread_stop_event.set()
        logging.getLogger('root_logger').info(f'[EMULATOR {self.name}]: Thread ended.')

    def set_value(self, value):
        self.module_thread.set_value(value)


class RandomThread(Thread):
    def __init__(self, mac, app, thread_stop_event, mqtt_client):
        self.thread_stop_event = thread_stop_event
        self.app = app
        self.module_mac = mac
        self.value = random.randint(1, 10)
        self.mqtt_client = mqtt_client
        self.mqtt_client.subscribe(mac)
        super(RandomThread, self).__init__()

    def set_value(self, value):
        self.value = value

    def run(self):
        while not self.thread_stop_event.isSet():
            data = {
                "module_mac": self.module_mac,
                "values": {},
            }

            with self.app.app_context():
                module = Module.query.filter_by(mac=self.module_mac).first()
                devices = module.devices

                for device in devices:
                    data['values'][str(device.id)] = {
                        'value': random.randint((self.value * 100) - 10, (self.value * 100) + 10) / 100,
                        'unit': 'value',
                        'writable': True
                    }

            self.mqtt_client.publish('brewmaster-backend', json.dumps(data))
            time.sleep(1)
