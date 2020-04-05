from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Datatype(StandardModel):

    __tablename__ = 'datatypes'

    name = db.Column(db.String(100), nullable=True)

    protocol_id = db.Column(UUID(as_uuid=True), db.ForeignKey('protocols.id'))
    protocols = db.relationship("Protocol", back_populates="datatype")

    def summary(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            protocols=self.protocols.summary() if self.protocols else None
        )
