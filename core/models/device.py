from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Device(StandardModel):
    __tablename__ = 'devices'

    fk_module = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id'))
    module = db.relationship("Module", back_populates="devices")

    uuid = db.Column(UUID(as_uuid=True), nullable=True)

    address = db.Column(db.String(100), nullable=True)
    poll_rate = db.Column(db.String(100), nullable=True)

    def summary(self) -> dict:
        return dict(
            id=self.id,
            uuid=self.uuid,
            address=self.address,
            poll_rate=self.poll_rate,
        )
