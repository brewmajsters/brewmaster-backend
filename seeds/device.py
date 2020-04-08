import random
import uuid

from flask_seeder import Seeder
from core.models import Module, Device


class DeviceSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 6

    def run(self):
        modules = Module.query.all()
        device_params = [
            {'uuid': 'b484aafb-7e1a-473a-9107-f8e08f904d6e', 'address': '127.0.0.1', 'poll_rate': '1'},
            {'uuid': '70140eb4-92b8-467c-aa3a-15b7bd104330', 'address': '127.0.0.1', 'poll_rate': '2'},
            {'uuid': 'f14dee0f-bd91-411f-8427-c0bd82e96220', 'address': '127.0.0.1', 'poll_rate': '3'}
        ]

        for param in device_params:
            device = Device(
                uuid=param.get('uuid'),
                address=param.get('address'),
                poll_rate=param.get('poll_rate'),
                module_id=random.choice(modules).id
            )
            print(f'Creating device: {device.uuid}')
            self.db.session.add(device)
