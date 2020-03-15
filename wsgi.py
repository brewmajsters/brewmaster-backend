import eventlet
from application import create_app, socketio

app = create_app()

if __name__ == "__main__":
    eventlet.monkey_patch()

    socketio.run(
        app,
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
        use_reloader=False
    )
