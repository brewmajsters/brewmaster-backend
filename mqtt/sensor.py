import logging
from random import random
from threading import Thread, Event
from mqtt.client import mqtt_client


class Sensor(object):
    def __init__(self, name, socket_io):
        self.thread = Thread()
        self.thread_stop_event = Event()
        self.name = name
        self.socket_io = socket_io

    def run(self):
        mqtt_client.subscribe(self.name)

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

    def random_number_generator(self):
        while not self.thread_stop_event.isSet():
            number = round(random() * 10, 3)
            mqtt_client.publish(self.sensor_name, str(number))
            self.socket_io.sleep(self.delay)

    def run(self):
        self.random_number_generator()
