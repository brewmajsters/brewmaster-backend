import os
from flask_migrate import Manager, Migrate, MigrateCommand
from wsgi import app
from core.models.base_model import db


app.config.from_object(os.getenv('APP_SETTINGS'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
