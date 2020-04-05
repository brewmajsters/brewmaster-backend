import json
from flask import Blueprint, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
from api import http_status
from api.errors import ApiException, ValidationException
from api.forms.module_form import ModuleSetValueForm
from core.models import Module, DeviceTypeDatapoint
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


# DATAPOINTS
@blueprint.route('/datapoints', methods=['GET'])
def list_datapoints():
    datapoints = DeviceTypeDatapoint.query.all()
    return json.dumps(
        datapoints
    ), 200, {'ContentType': 'application/json'}


# MODULES
@blueprint.route('/modules/<module_id>/set_value', methods=['POST'])
def set_module_value(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data = form.data
    return json.dumps(data), 200, {'ContentType': 'application/json'}
