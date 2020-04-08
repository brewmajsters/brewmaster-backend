import random
from flask_seeder import Seeder
from core.models import DeviceTypeDatapoint, ModuleDeviceType


class DeviceTypeDatapointSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    def run(self):
        module_device_types = ModuleDeviceType.query.all()
        data_point_params = [
            {'name': 'Heater', 'units': 'Celsius', 'code': '227', 'legend': 'H', 'writable': True},
            {'name': 'Motor', 'units': 'Meter per second', 'code': '974', 'legend': 'M', 'writable': True},
            {'name': 'Heat Sensor', 'units': 'Celsius', 'code': '113', 'legend': 'HS', 'writable': False}
        ]

        for param in data_point_params:
            device_type_datapoint = DeviceTypeDatapoint(
                name=param.get('name'),
                units=param.get('units'),
                code=param.get('code'),
                legend=param.get('legend'),
                writable=param.get('writable'),
                module_device_type_id=random.choice(module_device_types).id,
            )
            print(f'Creating device type datapoint: {device_type_datapoint.name}')
            self.db.session.add(device_type_datapoint)
