from flask import Flask
from flask_cors import CORS
from api import routes
from api.errors import register_error_handlers
from web_socket.events import socketio
from core.handlers.db_handler import init_logger
from core.models.abstract.base_model import initialize_db
from mqtt.client import mqtt_client


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('settings.development.DevelopmentConfig')

    # Create CORS
    CORS(app)

    # Register custom error handlers
    register_error_handlers(app)

    # Create routes
    app.register_blueprint(routes.blueprint)

    # Initializing database
    initialize_db(app)

    # Initializing logger
    init_logger()

    # Initializing mqtt
    mqtt_client.init(app, socketio)
    mqtt_client.connect()

    # Initializing socketio
    socketio.init_app(app)

    return app
