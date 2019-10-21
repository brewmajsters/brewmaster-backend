from core.models.base_model import BaseModel, db


class Sensor(BaseModel):
    __tablename__ = 'sensors'

    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
