import typing

from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Device(StandardModel):
    __tablename__ = 'devices'

    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    poll_rate = db.Column(db.Integer(), nullable=False)
    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id'))

    module = db.relationship("Module", back_populates="devices")
    device_datapoints = db.relationship("DeviceDatapoint", lazy='dynamic', back_populates="device")

    def get_device_datapoints(self) -> typing.List:
        return self.module.module_device_type.device_type_datapoints

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            module_id=str(self.module_id) if self.module_id else None,
            name=str(self.name),
            address=self.address,
            poll_rate=self.poll_rate,
            datapoints=[datapoint.summary() for datapoint in self.get_device_datapoints()]
        )

    def module_summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=str(self.name),
            address=self.address,
            poll_rate=self.poll_rate,
        )
