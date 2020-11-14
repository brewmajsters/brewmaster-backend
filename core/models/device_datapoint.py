from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class DeviceDatapoint(StandardModel):
    __tablename__ = 'device_datapoint'

    name = db.Column(db.String(100))
    code = db.Column(db.String(100))
    description = db.Column(db.String(1024), nullable=True)
    writable = db.Column(db.Boolean)
    virtual = db.Column(db.Boolean)
    unit_symbol = db.Column(db.String(8), nullable=True)
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device.id'))

    device = db.relationship("Device", back_populates="device_datapoints")
    measurements = db.relationship("Measurement", back_populates="device_datapoint")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            device_id=str(self.device_id) if self.device else None,
            name=self.name,
            unit_symbol=self.unit_symbol,
            code=self.code,
            virtual=self.virtual,
            description=self.description,
            writable=self.writable,
        )
