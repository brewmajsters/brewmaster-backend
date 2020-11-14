from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class DeviceTypeDatapoint(StandardModel):
    __tablename__ = 'device_type_datapoint'

    name = db.Column(db.String(100))
    code = db.Column(db.String(100))
    description = db.Column(db.String(1024), nullable=True)
    writable = db.Column(db.Boolean)
    virtual = db.Column(db.Boolean)
    module_device_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('module_device_type.id'))
    unit_id = db.Column(UUID(as_uuid=True), db.ForeignKey('unit.id'), nullable=True)

    module_device_type = db.relationship("ModuleDeviceType", back_populates="device_type_datapoints")
    unit = db.relationship("Unit", back_populates="device_type_datapoints")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            module_device_type_id=str(self.module_device_type_id) if self.module_device_type else None,
            unit_id=str(self.unit_id) if self.unit else None,
            name=self.name,
            code=self.code,
            virtual=self.virtual,
            description=self.description,
            writable=self.writable,
        )
