import json
import logging
import time
from random import random
from threading import Thread, Event
from core.models import Module
from mqtt.emulator.client_emulator import mqtt_client_emulator


class ModuleEmulator(object):
    def __init__(self, name, app):
        self.thread = Thread()
        self.thread_stop_event = Event()
        self.name = name
        self.app = app

    def run(self):
        if not self.thread.is_alive():
            thread = RandomThread(self.name, self.app, self.thread_stop_event)
            thread.start()
            logging.getLogger('root_logger').info(f'[EMULATOR {self.name}]: Thread started.')

    def stop(self):
        if self.thread.isAlive():
            self.thread_stop_event.set()
        logging.getLogger('root_logger').info(f'[EMULATOR {self.name}]: Thread ended.')


class RandomThread(Thread):
    def __init__(self, mac, app, thread_stop_event):
        self.thread_stop_event = thread_stop_event
        self.app = app
        self.module_mac = mac
        mqtt_client_emulator.subscribe(mac)
        super(RandomThread, self).__init__()

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
                        'value': round(random() * 10, 3),
                        'unit': 'value',
                        'writable': True
                    }

            mqtt_client_emulator.publish('brewmaster-backend', json.dumps(data))
            time.sleep(1)
