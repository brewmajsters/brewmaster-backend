import logging
from flask_socketio import SocketIO
from core.models import Module
from mqtt.sensor import Sensor

socketio = SocketIO(async_mode="eventlet")
sensors = []


@socketio.on('connect', namespace='/web_socket')
def on_connect():
    global sensors

    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully connected.')

    for module in Module.query.all():
        sensor = Sensor(module.mac, socketio)
        sensors.append(sensor)
        sensor.run()


@socketio.on('disconnect', namespace='/web_socket')
def on_disconnect():
    global sensors

    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully disconnected.')

    for sensor in sensors:
        sensor.stop()


@socketio.on('callback', namespace='/web_socket')
def on_callback(msg):
    logging.getLogger('root_logger').info(f'[SocketIO]: ACK: {msg}')
