from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class OneWire(StandardModel):
    __tablename__ = 'one_wires'

    unit_id = db.Column(db.String(100), nullable=True)
    pull_rate = db.Column(db.String(100), nullable=True)

    fk_device = db.Column(db.Integer, db.ForeignKey('devices.id'))

    device = db.relationship("Device", back_populates="one_wires")
