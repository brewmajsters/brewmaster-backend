from sqlalchemy import types

from core.models.base_model import BaseModel
from application import db


class Notification(BaseModel):
    __tablename__ = 'notifications'

    message = db.Column(db.String(100), nullable=True)
    method = db.Column(db.String(10), nullable=False, default='GET')
    url = db.Column(db.String(50), nullable=False, default='/')
    module = db.Column(db.String(50), nullable=False)
    function = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False, default='')
    status_code = db.Column(db.Integer, nullable=True)
    request = db.Column(types.JSON(), nullable=True)
    additional_data = db.Column(types.JSON(), nullable=True)
