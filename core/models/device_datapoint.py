from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class DeviceDatapoint(StandardModel):
    __tablename__ = 'device_datapoints'

    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)
    writable = db.Column(db.Boolean, nullable=False, default=True)
    virtual = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.String(300), nullable=True)
    unit_symbol = db.Column(db.String(20), nullable=False)
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey('devices.id'))

    device = db.relationship("Device", back_populates="device_type_datapoints")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
            code=self.code,
            writable=self.writable,
            virtual=self.virtual,
            description=self.description,
            unit_symbol=self.unit_symbol,
            device_id=str(self.device_id) if self.device_id else None,
        )
