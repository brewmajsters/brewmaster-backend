from core.models import Module
from mqtt.client import mqtt_client


def handle_mqtt_connections():
    modules = Module.query.all()

    for module in modules:
        mqtt_client.subscribe(module.mac)
