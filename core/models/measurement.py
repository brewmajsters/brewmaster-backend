import datetime

from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.timescale_model import TimeScaleModel


class Measurement(TimeScaleModel):
    __tablename__ = 'measurements'
    __timestamp_field__ = 'timestamp'

    timestamp = db.Column(db.DateTime, nullable=False, primary_key=True, default=datetime.datetime.utcnow)
    value = db.Column(db.String(250), nullable=False)
    device_datapoint_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device_datapoints.id'))

    device_datapoint = db.relationship("DeviceDatapoint", back_populates="measurements")

    def summary(self) -> dict:
        return dict(
            timestamp=self.timestamp,
            value=self.value,
            device_datapoint_id=str(self.device_datapoint_id) if self.device_datapoint_id else None,
        )
