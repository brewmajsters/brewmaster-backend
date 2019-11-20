from core.models import BaseModel
from core.models.abstract.base_model import db


class StandardModel(BaseModel):
    __abstract__ = True

    pk_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
