import datetime

from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.timescale_model import TimeScaleModel


class Measurement(TimeScaleModel):
    __tablename__ = 'measurement'

    time = db.Column(db.DateTime, primary_key=True, server_default=db.func.now())
    value = db.Column(db.String(256))
    device_datapoint_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device_datapoint.id'))

    device_datapoint = db.relationship("DeviceDatapoint", back_populates="measurements")

    def summary(self) -> dict:
        return dict(
            time=self.time,
            value=self.value,
            device_datapoint_id=str(self.device_datapoint_id)
        )

