from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Module(StandardModel):
    __tablename__ = 'modules'

    uuid = db.Column(db.String(100), nullable=True)

    fk_module_device_type = db.Column(db.Integer, db.ForeignKey('module_device_types.id'))
    module_device_type = db.relationship("ModuleDeviceType")
    devices = db.relationship("Device", back_populates="module")
