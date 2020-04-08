from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class DataType(StandardModel):
    __tablename__ = 'data_types'

    name = db.Column(db.String(100), nullable=True)

    protocols = db.relationship("Protocol", back_populates="datatype")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            name=self.name,
        )
