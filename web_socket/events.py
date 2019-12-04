import logging
from flask_socketio import SocketIO
from mqtt.sensor import Sensor


socketio = SocketIO(async_mode="eventlet")
sensors = [Sensor('heater', socketio), Sensor('pressure', socketio)]


@socketio.on('connect', namespace='/test_web_socket')
def on_connect():
    global sensors
    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully connected.')

    for sensor in sensors:
        sensor.run()


@socketio.on('disconnect', namespace='/test_web_socket')
def on_disconnect():
    global sensors
    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully disconnected.')

    for sensor in sensors:
        sensor.stop()


@socketio.on('callback', namespace='/test_web_socket')
def on_callback(msg):
    logging.getLogger('root_logger').info(f'[SocketIO]: ACK: {msg}')
