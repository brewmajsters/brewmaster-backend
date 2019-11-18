"""App entry point."""
from application import create_app

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(
        app,
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
        use_reloader=False
    )
