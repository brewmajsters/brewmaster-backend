from flask_seeder import Seeder
from core.models import DataType


class DataTypeSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        data_type_names = ['Integer', 'String', 'Float', 'Boolean']

        for name in data_type_names:
            data_type = DataType(name=name)
            print(f'Creating data_type: {data_type.name}')
            self.db.session.add(data_type)
