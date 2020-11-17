import typing

from sqlalchemy.dialects.postgresql import UUID

from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Unit(StandardModel):
    __tablename__ = 'unit'

    name = db.Column(db.String(100), unique=True)
    symbol = db.Column(db.String(8), unique=True)

    device_type_datapoints = db.relationship("DeviceTypeDatapoint", back_populates="unit")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
            symbol=self.symbol,
        )
