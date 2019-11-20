from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Device(StandardModel):
    __tablename__ = 'devices'

    fk_module = db.Column(db.Integer, db.ForeignKey('modules.pk_id'))
    module = db.relationship("Module", back_populates="devices")

    gpios = db.relationship("Gpio", back_populates="device")
    modbus_rtus = db.relationship("ModbusRtu", back_populates="device")
    one_wires = db.relationship("OneWire", back_populates="device")

