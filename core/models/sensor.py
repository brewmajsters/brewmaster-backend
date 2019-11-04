from core.models.base_model import db
from core.models.base_timescale_model import BaseTimeScaleModel


class Sensor(BaseTimeScaleModel):
    __tablename__ = 'sensors'

    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
