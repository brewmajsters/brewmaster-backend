from flask import Flask
from api import routes
from api.events import socketio
from core.handlers.db_handler import init_logger
from core.models.abstract.base_model import db, initialize_db
from mqtt.client import mqtt_client


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('settings.development.DevelopmentConfig')

    # Create routes
    app.register_blueprint(routes.blueprint)

    mqtt_client.init(app)
    socketio.init_app(app)
    initialize_db(app)

    # Initializing logger
    init_logger()

    mqtt_client.connect()

    return app
