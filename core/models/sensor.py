import datetime
from psycopg2._psycopg import DatabaseError
from sqlalchemy import event, DDL
from api import http_status
from api.errors import ApiException
from core.models.abstract.base_model import db


class Sensor(db.Model):
    __tablename__ = 'sensors'
    __timestamp_field__ = 'time'

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ApiException(
                f'Vyskytla sa chyba pri vytvorení záznamu: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )

    time = db.Column(db.DateTime, nullable=False, primary_key=True, default=datetime.datetime.utcnow)
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

