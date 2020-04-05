from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class ModuleDeviceType(StandardModel):
    __tablename__ = 'module_device_types'

    fk_protocol = db.Column(UUID(as_uuid=True), db.ForeignKey('protocols.id'))
    protocol = db.relationship("Protocol")

    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    code = db.Column(db.String(100), nullable=True)

    def summary(self) -> dict:
        return dict(
            id=self.id,
            code=self.code,
            model=self.model,
            manufacturer=self.manufacturer,
            address_datatype=self.address_datatype.summary()
        )
