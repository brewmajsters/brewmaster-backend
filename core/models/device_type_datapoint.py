from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class DeviceTypeDatapoint(StandardModel):
    __tablename__ = 'device_type_datapoints'

    name = db.Column(db.String(100), nullable=True)
    units = db.Column(db.String(100), nullable=True)
    datapoint_code = db.Column(db.String(100), nullable=True)
    writable = db.Column(db.Boolean, nullable=True)

    fk_module_device_type = db.Column(db.Integer, db.ForeignKey('module_device_types.pk_id'))
    module_device_type = db.relationship("ModuleDeviceType")
