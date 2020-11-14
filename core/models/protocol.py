from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Protocol(StandardModel):
    __tablename__ = 'protocol'

    name = db.Column(db.String(100), unique=True)

    module_device_types = db.relationship("ModuleDeviceType", back_populates="protocol")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
        )
