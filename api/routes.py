import json

from flask import Blueprint, render_template
from mqtt.client import mqtt_client

blueprint = Blueprint('blueprint', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/test_mqtt', methods=['GET'])
def test_mqtt():
    name = "mqtt_sensor"
    message = "mqtt_test"
    mqtt_client.subscribe(name)
    mqtt_client.publish(name, message)
    return f'published to: {name} with message: {message}'


@blueprint.route('/test_web', methods=['GET'])
def test_all():
    return render_template('test.html')


@blueprint.route('/test_cors', methods=['GET'])
def test_cors():
    return json.dumps(
        {'success': True}
    ), 200, {'ContentType': 'application/json'}
