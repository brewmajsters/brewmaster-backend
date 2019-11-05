from sqlalchemy import event, DDL

from core.models.base_model import db


class Sensor(db.Model):
    __tablename__ = 'sensors'
    __timestamp_field__ = 'time'

    time = db.Column(db.Date, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)


trigger = DDL(
    f"SELECT create_hypertable('sensors', 'time');"
)

event.listen(
Sensor.__table__,
    'after_create',
    trigger.execute_if(dialect='postgresql')
)

