import json
from flask import Blueprint, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
from api import http_status
from api.errors import ApiException, ValidationException
from api.forms.module_form import ModuleSetValueForm
from core.models import Module, DeviceTypeDatapoint, Protocol, Device, ModuleDeviceType, DataType
from mqtt.client import mqtt_client
from mqtt.errors import MQTTException

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


# DEVICE_TYPE_DATAPOINT
@blueprint.route('/datapoints', methods=['GET'])
def list_datapoints():
    datapoints = DeviceTypeDatapoint.query.all()
    return json.dumps(
        [item.summary() for item in datapoints]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/datapoints/<datapoint_id>', methods=['GET'])
def get_datapoint(datapoint_id):
    datapoint = DeviceTypeDatapoint.query.filter(DeviceTypeDatapoint.id == datapoint_id).first()
    return json.dumps(
        datapoint.summary()
    ), 200, {'ContentType': 'application/json'}


# DATATYPE
@blueprint.route('/datatypes', methods=['GET'])
def list_datatypes():
    datatypes = DataType.query.all()
    return json.dumps(
        [item.summary() for item in datatypes]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/datatypes/<datatypes_id>', methods=['GET'])
def get_datatype(datatypes_id):
    datatype = DataType.query.filter(DataType.id == datatypes_id).first()
    return json.dumps(
        datatype.summary()
    ), 200, {'ContentType': 'application/json'}


# MODULE_DEVICE_TYPE
@blueprint.route('/devicetypes', methods=['GET'])
def list_device_types():
    module_device_types = ModuleDeviceType.query.all()
    return json.dumps(
        [item.summary() for item in module_device_types]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/devicetypes/<device_type_id>', methods=['GET'])
def get_device_type(device_type_id):
    module_device_type = ModuleDeviceType.query.filter(ModuleDeviceType.id == device_type_id).first()
    return json.dumps(
        module_device_type.summary()
    ), 200, {'ContentType': 'application/json'}


# PROTOCOLS
@blueprint.route('/protocols', methods=['GET'])
def list_protocols():
    protocols = Protocol.query.all()
    return json.dumps(
        [item.summary() for item in protocols]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/protocols/<protocol_id>', methods=['GET'])
def get_protocol(protocol_id):
    protocol = Protocol.query.filter(Protocol.id == protocol_id).first()
    return json.dumps(
        protocol.summary()
    ), 200, {'ContentType': 'application/json'}


# DEVICES
@blueprint.route('/devices', methods=['GET'])
def list_devices():
    devices = Device.query.all()
    return json.dumps(
        [item.summary() for item in devices]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/devices/<devices_id>', methods=['GET'])
def get_device(devices_id):
    device = Device.query.filter(Device.id == devices_id).first()
    return json.dumps(
        device.summary()
    ), 200, {'ContentType': 'application/json'}


# MODULES
@blueprint.route('/modules', methods=['GET'])
def list_modules():
    modules = Module.query.all()
    return json.dumps(
        [item.summary() for item in modules]
    ), 200, {'ContentType': 'application/json'}


@blueprint.route('/modules/<module_id>', methods=['GET'])
def get_module(module_id):
    module = Module.query.filter(Module.id == module_id).first()
    return json.dumps(
        module.summary()
    ), 200, {'ContentType': 'application/json'}


# MODULES_OPERATIONS
@blueprint.route('/modules/request', methods=['POST'])
def request_all(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    modules = Module.query.all()
    if not modules:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data = form.data
    return json.dumps(data), 200, {'ContentType': 'application/json'}


@blueprint.route('/modules/<module_id>/request', methods=['POST'])
def request_module(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data = form.data
    return json.dumps(data), 200, {'ContentType': 'application/json'}


@blueprint.route('/modules/<module_id>/update', methods=['POST'])
def update_module(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data = form.data
    return json.dumps(data), 200, {'ContentType': 'application/json'}


@blueprint.route('/modules/<module_id>/set_value', methods=['POST'])
def set_value_module(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    data = form.data

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    device = module.devices.filter_by(id=data.get('device_id')).first()
    if not device:
        raise ApiException('Dané zariadenie sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data['device_uuid'] = data['device_id']
    del data['device_id']

    # TODO: Ziskat sequence number (odniekial)
    data['sequence_number'] = 123

    try:
        response = mqtt_client.send_message(module.mac, json.dumps(data))
    except MQTTException as e:
        raise ApiException(e.message, status_code=http_status.HTTP_400_BAD_REQUEST, previous=e)

    return json.dumps(response), 200, {'ContentType': 'application/json'}


@blueprint.route('/modules/<module_id>/config', methods=['POST'])
def config_module(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetValueForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data = form.data
    return json.dumps(data), 200, {'ContentType': 'application/json'}
