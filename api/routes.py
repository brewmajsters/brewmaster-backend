import json
from random import randint

from flask import Blueprint, request
from werkzeug.datastructures import ImmutableMultiDict
from api import http_status
from api.errors import ApiException, ValidationException
from api.forms.device_datapoint_put import DeviceDatapointPutForm
from api.forms.module_set_config import ModuleSetConfigForm
from api.forms.module_set_value import ModuleSetValueForm
from core.models import (
    Unit,
    Module,
    DeviceTypeDatapoint,
    DeviceDatapoint,
    Protocol,
    Device,
    ModuleDeviceType,
    Measurement
)
from mqtt.client import mqtt_client
from mqtt.errors import MQTTException

blueprint = Blueprint('blueprint', __name__, template_folder='templates', static_folder='static')

# UNIT
@blueprint.route('/units', methods=['GET'])
def list_units():
    units = Unit.query.all()
    return json.dumps(
        [item.summary() for item in units]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/units/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    unit = Unit.query.filter(Unit.id == unit_id).first()
    return json.dumps(
        unit.summary()
    ), 200, {'Content-Type': 'application/json'}

# DEVICE_TYPE_DATAPOINT
@blueprint.route('/devicetype_datapoints', methods=['GET'])
def list_devicetype_datapoints():
    devicetype_datapoints = DeviceTypeDatapoint.query.all()
    return json.dumps(
        [item.summary() for item in devicetype_datapoints]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/devicetype_datapoints/<devicetype_datapoint_id>', methods=['GET'])
def get_devicetype_datapoint(devicetype_datapoint_id):
    devicetype_datapoint = DeviceTypeDatapoint.query.filter(DeviceTypeDatapoint.id == devicetype_datapoint_id).first()
    return json.dumps(
        devicetype_datapoint.summary()
    ), 200, {'Content-Type': 'application/json'}

# MODULE_DEVICE_TYPE
@blueprint.route('/devicetypes', methods=['GET'])
def list_device_types():
    module_device_types = ModuleDeviceType.query.all()
    return json.dumps(
        [item.summary() for item in module_device_types]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/devicetypes/<device_type_id>', methods=['GET'])
def get_device_type(device_type_id):
    module_device_type = ModuleDeviceType.query.filter(ModuleDeviceType.id == device_type_id).first()
    return json.dumps(
        module_device_type.summary()
    ), 200, {'Content-Type': 'application/json'}

# PROTOCOLS
@blueprint.route('/protocols', methods=['GET'])
def list_protocols():
    protocols = Protocol.query.all()
    return json.dumps(
        [item.summary() for item in protocols]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/protocols/<protocol_id>', methods=['GET'])
def get_protocol(protocol_id):
    protocol = Protocol.query.filter(Protocol.id == protocol_id).first()
    return json.dumps(
        protocol.summary()
    ), 200, {'Content-Type': 'application/json'}

# MODULES
@blueprint.route('/modules', methods=['GET'])
def list_modules():
    modules = Module.query.all()
    return json.dumps(
        [item.summary() for item in modules]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/modules/<module_id>', methods=['GET'])
def get_module(module_id):
    module = Module.query.filter(Module.id == module_id).first()

    return json.dumps(
        module.summary()
    ), 200, {'Content-Type': 'application/json'}

# DEVICES
@blueprint.route('/devices', methods=['GET'])
def list_devices():
    module_id = request.args.get('module_id')

    if module_id:
        module = Module.query.get(module_id)
        if not module:
            raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

        devices = Device.query.filter(Device.module == module)
    else:
        devices = Device.query.all()
    return json.dumps(
        [item.summary() for item in devices]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.filter(Device.id == device_id).first()
    return json.dumps(
        device.summary()
    ), 200, {'Content-Type': 'application/json'}

# DEVICE_DATAPOINT
@blueprint.route('/device_datapoints', methods=['GET'])
def list_device_datapoints():
    device_id = request.args.get('device_id')

    if device_id:
        device = Device.query.get(device_id)
        if not device:
            raise ApiException('Daný device sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

        datapoints = DeviceDatapoint.query.filter(DeviceDatapoint.device == device)
    else:
        datapoints = DeviceDatapoint.query.all()

    return json.dumps(
        [item.summary() for item in datapoints]
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/device_datapoints/<datapoint_id>', methods=['GET'])
def get_device_datapoint(datapoint_id):
    datapoint = DeviceDatapoint.query.filter(DeviceDatapoint.id == datapoint_id).first()
    if not datapoint:
        raise ApiException('Daný datapoint sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    return json.dumps(
        datapoint.summary()
    ), 200, {'Content-Type': 'application/json'}

@blueprint.route('/device_datapoints/<datapoint_id>', methods=['PATCH'])
def set_device_datapoint(datapoint_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    response = {'result': 'ok'}
    # form = DeviceDatapointPutForm(json_data, meta={'csrf': False})

    # if not form.validate():
    #     raise ValidationException(form.errors)

    datapoint = DeviceDatapoint.query.filter(DeviceDatapoint.id == datapoint_id).first()
    if not datapoint:
        raise ApiException('Daný datapoint sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    if 'value' in json_data and datapoint.writable:
        value = json_data.get('value')

        if not datapoint.virtual:
            sequence_number = randint(0, 65535)
            request_data = {
                'device_id': str(datapoint.device.id),
                'datapoint': datapoint.code,
                'value': f'{value}',
                'sequence_number': sequence_number
            }

            try:
                response = mqtt_client.send_message(
                    datapoint.device.module.mac,
                    'SET_VALUE',
                    json.dumps(request_data)
                )
            except MQTTException as e:
                raise ApiException(e.message, status_code=http_status.HTTP_400_BAD_REQUEST, previous=e)

            del json_data['value']

    elif 'value' in json_data and not datapoint.writable:
        raise ApiException('Specified value for non-writable datapoint.', status_code=http_status.HTTP_400_BAD_REQUEST)

    datapoint.update(json_data)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}

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
    return json.dumps(data), 200, {'Content-Type': 'application/json'}

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
    return json.dumps(data), 200, {'Content-Type': 'application/json'}

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
    return json.dumps(data), 200, {'Content-Type': 'application/json'}

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
    del data['device_id']
    if not device:
        raise ApiException('Dané zariadenie sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    datapoint = module.module_device_type.device_type_datapoints.filter_by(code=data.get('datapoint')).first()
    if not datapoint:
        raise ApiException('Daný datapoint sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    data['device_uuid'] = str(device.uuid)
    data['sequence_number'] = randint(100, 999)

    try:
        response = mqtt_client.send_message(module.mac, 'SET_VALUE', json.dumps(data))
    except MQTTException as e:
        raise ApiException(e.message, status_code=http_status.HTTP_400_BAD_REQUEST, previous=e)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}

@blueprint.route('/modules/<module_id>/config', methods=['POST'])
def config_module(module_id):
    json_data = ImmutableMultiDict(request.get_json(force=True))
    form = ModuleSetConfigForm(json_data, meta={'csrf': False})

    if not form.validate():
        raise ValidationException(form.errors)

    request_data = form.data

    module = Module.query.get(module_id)
    if not module:
        raise ApiException('Daný modul sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    device = module.devices.filter_by(id=request_data.get('device_id')).first()
    if not device:
        raise ApiException('Dané zariadenie sa nepodarilo nájsť.', status_code=http_status.HTTP_404_NOT_FOUND)

    device.poll_rate = request_data.get('poll_rate')
    device.save()

    data = {
        str(device.uuid): {
            'address': request_data.get('address'),
            'poll_rate': request_data.get('poll_rate')
        }
    }

    try:
        response = mqtt_client.send_message(module.mac, 'SET_CONFIG', json.dumps(data))
    except MQTTException as e:
        raise ApiException(e.message, status_code=http_status.HTTP_400_BAD_REQUEST, previous=e)

    return json.dumps(response), 200, {'Content-Type': 'application/json'}
