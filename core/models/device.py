from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Device(StandardModel):
    __tablename__ = 'devices'

    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id'))
    uuid = db.Column(UUID(as_uuid=True), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    poll_rate = db.Column(db.String(100), nullable=True)

    module = db.relationship("Module", back_populates="devices")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            module_id=str(self.module_id) if self.module_id else None,
            uuid=str(self.uuid),
            address=self.address,
            poll_rate=self.poll_rate,
        )
