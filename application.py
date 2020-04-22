import os
from flask import Flask
from flask_cors import CORS
from api import routes
from api.errors import register_error_handlers
from web_socket.events import socketio
from core.handlers.db_handler import init_logger
from core.models.abstract.base_model import initialize_db
from mqtt.client import mqtt_client
from mqtt.emulator.client_emulator import mqtt_client_emulator


# Constructing the core application
def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Application environment configuration
    app.config.from_object('settings.base.BaseConfig')

    if os.getenv('RUN_ENVIRONMENT') == 'production':
        app.config.from_object('settings.production.ProductionConfig')

    elif os.getenv('RUN_ENVIRONMENT') == 'development':
        app.config.from_object('settings.development.DevelopmentConfig')

    # Create CORS Headers
    CORS(app)

    # Register custom error handlers
    register_error_handlers(app)

    # Create routes
    app.register_blueprint(routes.blueprint)

    # Initializing database
    initialize_db(app)

    # Initializing logger
    init_logger()

    # Initializing mqtt client
    mqtt_client.init(app, socketio)
    # Connecting mqtt client to broker
    mqtt_client.connect()
    # Making connections to mqtt modules
    mqtt_client.start_mqtt_connections()

    # Creating emulator modules when development settings are active
    if app.config.get('TESTING'):
        mqtt_client_emulator.init(app)
        mqtt_client_emulator.connect()
        mqtt_client_emulator.generate_modules()

    # Initializing socketio client
    socketio.init_app(app)

    return app
