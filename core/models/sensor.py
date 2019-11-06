import datetime
from core.models.abstract.base_model import db
from core.models.abstract.timescale_model import TimeScaleModel


class Sensor(TimeScaleModel):
    __tablename__ = 'sensors'
    __timestamp_field__ = 'time'

    time = db.Column(db.DateTime, nullable=False, primary_key=True, default=datetime.datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
