import logging
from flask_socketio import SocketIO

socketio = SocketIO(async_mode="eventlet", cors_allowed_origins="*")


@socketio.on('connect', namespace='/web_socket')
def on_connect():
    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully connected.')


@socketio.on('disconnect', namespace='/web_socket')
def on_disconnect():
    logging.getLogger('root_logger').info(f'[SocketIO]: Client successfully disconnected.')


@socketio.on('callback', namespace='/web_socket')
def on_callback(msg):
    logging.getLogger('root_logger').info(f'[SocketIO]: ACK: {msg}')
