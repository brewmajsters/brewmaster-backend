import random
from flask_seeder import Seeder
from core.models import DataType, Protocol


class ProtocolSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        data_types = DataType.query.all()
        protocol_names = ['Protocol1', 'Protocol2', 'Protocol3']

        for name in protocol_names:
            protocol = Protocol(name=name, datatype_id=random.choice(data_types).id)
            print(f'Creating protocol: {protocol.name}')
            self.db.session.add(protocol)
