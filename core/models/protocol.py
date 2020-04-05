from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Protocol(StandardModel):
    __tablename__ = 'protocols'

    name = db.Column(db.String(100), nullable=True)

    address_datatype = db.relationship("Datatype", back_populates="protocol")
