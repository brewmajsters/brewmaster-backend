from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Protocol(StandardModel):
    __tablename__ = 'protocols'

    name = db.Column(db.String(100), nullable=True)

    module_device_types = db.relationship("ModuleDeviceType", lazy='dynamic', back_populates="protocol")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
        )
