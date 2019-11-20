from flask import Flask
from flask_socketio import SocketIO
from core.models.abstract.base_model import db
from mqtt.client import MqttClient

mqtt_client = MqttClient()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('settings.development.DevelopmentConfig')

    with app.app_context():
        # Import parts of our application
        from api import routes
        from core.handlers.db_handler import init_logger
        # Create routes
        app.register_blueprint(routes.blueprint)

        db.init_app(app)
        mqtt_client.init(app)
        socketio = SocketIO(app)

        # Create tables for our models
        db.create_all()

        # Initializing logger
        init_logger()

        mqtt_client.connect()

    return app, socketio
