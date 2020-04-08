import random
from flask_seeder import Seeder
from core.models import ModuleDeviceType, Module


class ModuleSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    def run(self):
        module_device_types = ModuleDeviceType.query.all()
        module_macs = ['C9:65:6E:EA:B0:8B', 'E0:D5:1B:08:C9:EB', '4F:8E:91:81:60:91']

        for mac in module_macs:
            module = Module(
                mac=mac,
                module_device_type_id=random.choice(module_device_types).id
            )
            print(f'Creating module: {module.mac}')
            self.db.session.add(module)
