from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Datatype(StandardModel):
    __tablename__ = 'datatypes'

    name = db.Column(db.String(100), nullable=True)

    fk_protocol = db.Column(UUID(as_uuid=True), db.ForeignKey('protocols.id'))
    protocol = db.relationship("Protocol", back_populates="address_datatype")
