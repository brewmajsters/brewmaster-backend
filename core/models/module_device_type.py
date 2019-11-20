from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class ModuleDeviceType(StandardModel):
    __tablename__ = 'module_device_types'

    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    module_type_code = db.Column(db.String(100), nullable=True)

    fk_protocol = db.Column(db.Integer, db.ForeignKey('protocols.pk_id'))
    protocol = db.relationship("Protocol")
