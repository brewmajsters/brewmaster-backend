import datetime

from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.timescale_model import TimeScaleModel


class Measurement(TimeScaleModel):
    __tablename__ = 'measurement'

    time = db.Column(db.DateTime, primary_key=True, default=datetime.datetime.utcnow)
    value = db.Column(db.String(256))
    device_datapoint_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device_datapoint.id'))

    device_datapoint = db.relationship("DeviceDatapoint", back_populates="measurements")
