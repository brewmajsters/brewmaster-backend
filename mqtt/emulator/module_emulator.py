import json
import logging
import random
import time
from threading import Thread, Event
from core.models import Module


class ModuleEmulator(object):
    def __init__(self, mac, app, mqtt_client):
        self.mqtt_client = mqtt_client
        self.mac = mac
        self.app = app
        self.module_thread = None
        self.thread_stop_event = Event()

    def run(self):
        if not self.module_thread or not self.module_thread.is_alive():
            # Creating module thread
            self.module_thread = ModuleThread(self.mac, self.app, self.thread_stop_event, self.mqtt_client)
            self.module_thread.start()

            logging.getLogger('root_logger').info(f'[EMULATOR {self.mac}]: THREAD STARTED.')

    def stop(self):
        if self.module_thread.isAlive():
            self.thread_stop_event.set()
        logging.getLogger('root_logger').info(f'[EMULATOR {self.mac}]: THREAD STOPPED.')

    def set_value(self, data):
        self.module_thread.set_value(data)


class ModuleThread(Thread):
    def __init__(self, mac, app, thread_stop_event, mqtt_client):
        self.thread_stop_event = thread_stop_event
        self.app = app

        self.module = Module.query.filter_by(mac=mac).first()
        self.devices = self._init_devices()

        self.mqtt_client = mqtt_client
        self.mqtt_client.subscribe(mac)

        super(ModuleThread, self).__init__()

    def _init_devices(self):
        devices = self.module.devices
        return [{'device': device, 'value': random.randint(1, 10)} for device in devices]

    def set_value(self, data):
        for device in self.devices:
            emulator_device_uuid = str(device.get('device').id)
            data_device_uuid = data.get('device_uuid')

            if emulator_device_uuid == data_device_uuid:
                device['value'] = data.get('value')

    def run(self):
        while not self.thread_stop_event.isSet():
            data = {
                "module_mac": self.module.mac,
                "values": {}
            }

            with self.app.app_context():
                for device in self.devices:
                    datapoints = device.get('device').get_device_datapoints()
                    device_id = str(device.get('device').id)
                    device_value = device.get('value')

                    data['values'][device_id] = {
                        {
                            datapoint.code:
                                random.randint((int(device_value) * 100) - 10, (int(device_value) * 100) + 10) / 100
                        } for datapoint in datapoints
                    }

            self.mqtt_client.publish('brewmaster-backend', json.dumps(data))
            time.sleep(1)
