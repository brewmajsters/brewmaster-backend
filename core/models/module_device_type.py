from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class ModuleDeviceType(StandardModel):
    __tablename__ = 'module_device_types'

    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    code = db.Column(db.String(100), nullable=True)
    protocol_id = db.Column(UUID(as_uuid=True), db.ForeignKey('protocols.id'))

    device_type_datapoints = db.relationship("DeviceTypeDatapoint", back_populates="module_device_type")
    protocol = db.relationship("Protocol", back_populates="module_device_types")
    modules = db.relationship("Module", back_populates="module_device_type")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            protocol_id=str(self.protocol_id),
            code=self.code,
            model=self.model,
            manufacturer=self.manufacturer,
        )
