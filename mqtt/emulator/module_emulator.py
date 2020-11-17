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

    def set_config(self, data):
        self.module_thread.set_config(data)


class ModuleThread(Thread):
    def __init__(self, mac, app, thread_stop_event, mqtt_client):
        self.thread_stop_event = thread_stop_event
        self.app = app

        self.module = Module.query.filter_by(mac=mac).first()
        self.devices = self._init_devices()

        self.mqtt_client = mqtt_client

        self.mqtt_client.subscribe(f'{mac}/REQUEST')
        self.mqtt_client.subscribe(f'{mac}/UPDATE_FW')
        self.mqtt_client.subscribe(f'{mac}/SET_VALUE')
        self.mqtt_client.subscribe(f'{mac}/SET_CONFIG')
        self.mqtt_client.subscribe(f'{mac}/ALL_MODULES')

        super(ModuleThread, self).__init__()

    def _init_devices(self):
        devices = self.module.devices
        return [{
            'device': device,
            'value': random.randint(1, 10),
            'poll_rate': None,
            'address': None,
            'datapoints': [datapoint.summary() for datapoint in device.device_datapoints]
        } for device in devices]

    def set_value(self, data):
        for device in self.devices:
            emulator_device_uuid = str(device.get('device').uuid)
            data_device_uuid = data.get('device_uuid')

            if emulator_device_uuid == data_device_uuid:
                device['value'] = data.get('value')

    def set_config(self, data):
        for device in self.devices:
            emulator_device_uuid = str(device.get('device').uuid)

            if emulator_device_uuid in data:
                device_data = data.get(emulator_device_uuid)

                # TODO: Nejako zasimulovat nastavenie configu

    def run(self):
        while not self.thread_stop_event.isSet():
            data = {
                'module_mac': self.module.mac,
                'values': {}
            }

            with self.app.app_context():
                for device in self.devices:
                    device_id = str(device.get('device').id)
                    datapoints = device.get('datapoints')
                    device_value = device.get('value')

                    datapoint_dict = {}
                    for datapoint in datapoints:
                        datapoint_dict[str(datapoint.get('code'))] = random.randint(
                                (int(device_value) * 100) - 10, (int(device_value) * 100) + 10
                            ) / 100

                    data['values'][device_id] = datapoint_dict

            self.mqtt_client.publish('VALUE_UPDATE', json.dumps(data))
            time.sleep(1)
