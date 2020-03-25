from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Gpio(StandardModel):
    __tablename__ = 'gpios'

    pin_number = db.Column(db.String(100), nullable=True)
    pull_rate = db.Column(db.String(100), nullable=True)
    fk_device = db.Column(UUID(as_uuid=True), db.ForeignKey('devices.id'))
    device = db.relationship("Device", back_populates="gpios")
