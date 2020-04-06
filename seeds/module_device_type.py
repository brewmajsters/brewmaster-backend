import random
from flask_seeder import Seeder
from core.models import Protocol, ModuleDeviceType


class ModuleDeviceTypeSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        protocols = Protocol.query.all()
        module_device_type_params = [
            {'manufacturer': 'tesla', 'model': 'TS112', 'code': '123456'},
            {'manufacturer': 'hp', 'model': 'VR689', 'code': '234567'},
            {'manufacturer': 'toshiba', 'model': 'QW288', 'code': '345678'}
        ]

        for param in module_device_type_params:
            module_device_type = ModuleDeviceType(
                manufacturer=param.get('manufacturer'),
                model=param.get('model'),
                code=param.get('code'),
                protocol_id=random.choice(protocols).id
            )
            print(f'Creating module device type: {module_device_type.model}')
            self.db.session.add(module_device_type)
