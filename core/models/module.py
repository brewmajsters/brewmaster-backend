from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Module(StandardModel):
    __tablename__ = 'module'

    mac = db.Column(db.String(100), unique=True)
    module_device_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('module_device_type.id'))

    devices = db.relationship("Device", back_populates="module")
    module_notification = db.relationship("ModuleNotification", lazy='dynamic', back_populates="module")
    module_device_type = db.relationship("ModuleDeviceType", back_populates="modules")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            module_device_type_id=str(self.module_device_type_id) if self.module_device_type_id else None,
            mac=self.mac,
            devices=[device.config_summary() for device in self.devices]
        )
