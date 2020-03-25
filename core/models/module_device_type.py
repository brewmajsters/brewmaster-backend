from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class ModuleDeviceType(StandardModel):
    __tablename__ = 'module_device_types'

    fk_protocol = db.Column(UUID(as_uuid=True), db.ForeignKey('protocols.id'))

    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    module_type_code = db.Column(db.String(100), nullable=True)
    protocol = db.relationship("Protocol")
