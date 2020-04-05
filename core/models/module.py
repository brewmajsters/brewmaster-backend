from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Module(StandardModel):
    __tablename__ = 'modules'

    mac = db.Column(db.String(100), nullable=True)

    module_device_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('module_device_types.id'))
    module_device_type = db.relationship("ModuleDeviceType")

    devices = db.relationship("Device", back_populates="module")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            module_device_type_id=str(self.module_device_type.id) if self.module_device_type else None,
            mac=self.mac,
            devices=[item.summary() for item in self.devices]
        )

