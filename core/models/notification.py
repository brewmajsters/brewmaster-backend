from core.models.base_model import BaseModel
from application import db


class Notification(BaseModel):
    __tablename__ = 'notifications'

    message = db.Column(db.String(100), nullable=True)
