import logging
from random import random
from threading import Thread, Event
from time import sleep
from wsgi import socketio

thread = Thread()
thread_stop_event = Event()


class SocketIOClient(object):
    def __init__(self):
        self.connected_clients = {}

    @socketio.on('connect', namespace='/test')
    def on_connect(self, **kwargs):
        global thread
        logging.getLogger('root_logger').info(f'Client successfully connected.')

        if not thread.is_alive():
            thread = RandomThread()
            thread.start()

    @socketio.on('disconnect')
    def on_disconnect(self, **kwargs):
        logging.getLogger('root_logger').info(f'Client successfully disconnected.')


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def random_number_generator(self):
        logging.getLogger('root_logger').info(f'Making random numbers...')

        while not thread_stop_event.is_set():
            number = round(random() * 10, 3)
            socketio.emit('new_number',  {'number': number}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.random_number_generator()
