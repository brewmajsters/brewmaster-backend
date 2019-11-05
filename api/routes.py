"""Routes for main pages."""
from flask import Blueprint

from api.errors import ApiException
from application import mqtt_client

blueprint = Blueprint('blueprint', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/subscribe/<string:name>/', methods=['GET'])
def subscribe(name):
    mqtt_client.subscribe(name)
    return f'subscribed {name}'


@blueprint.route('/publish/<string:name>/<string:message>/', methods=['GET'])
def publish(name, message):
    mqtt_client.publish(name, message)
    return f'published to: {name} with message: {message}'

@blueprint.route('/test', methods=['GET'])
def test():
    name = "mqqt"
    message = "tvoja manka"
    mqtt_client.subscribe(name)
    mqtt_client.publish(name, message)
    return f'published to: {name} with message: {message}'
