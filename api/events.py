import logging
from random import random
from threading import Thread, Event
from flask_socketio import SocketIO

thread = Thread()
thread_stop_event = Event()
socketio = SocketIO(async_mode="eventlet")


@socketio.on('connect', namespace='/test_web_socket')
def on_connect():
    global thread
    logging.getLogger('root_logger').info(f'Client successfully connected.')

    if not thread.is_alive():
        thread = RandomThread()
        thread.start()
        print('thread started!')


@socketio.on('say', namespace='/test_web_socket')
def say():
    logging.getLogger('root_logger').info(f'SAYS!!!!!!!!!!!!!!')


@socketio.on('disconnect', namespace='/test_web_socket')
def on_disconnect():
    global thread_stop_event

    logging.getLogger('root_logger').info(f'Client successfully disconnected.')

    if thread.isAlive():
        thread_stop_event.set()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def random_number_generator(self):
        logging.getLogger('root_logger').info(f'Making random numbers...')

        while not thread_stop_event.isSet():
            number = round(random() * 10, 3)
            print(number)
            socketio.emit('new_number',  {'number': number}, namespace='/test_web_socket')
            print('sended.')
            socketio.sleep(self.delay)

    def run(self):
        self.random_number_generator()
