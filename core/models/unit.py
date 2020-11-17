from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Unit(StandardModel):
    __tablename__ = 'units'

    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(20), unique=True, nullable=False)

    device_type_datapoints = db.relationship("DeviceTypeDatapoint", lazy='dynamic', back_populates="unit")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
        )
