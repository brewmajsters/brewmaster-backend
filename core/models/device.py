import typing

from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Device(StandardModel):
    __tablename__ = 'device'

    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    poll_rate = db.Column(db.Integer())
    protocol_name = db.Column(db.String(100))
    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id'))

    module = db.relationship("Module", back_populates="devices")
    device_datapoints = db.relationship("DeviceDatapoint", back_populates="device")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
            module_id=str(self.module_id) if self.module_id else None,
            protocol_name=self.protocol_name,
            address=self.address,
            poll_rate=self.poll_rate,
        )

    def config_summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
            address=self.address,
            poll_rate=self.poll_rate,
        )
