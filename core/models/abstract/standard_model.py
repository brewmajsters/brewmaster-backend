from sqlalchemy.dialects.postgresql import UUID
from core.models import BaseModel
from core.models.abstract.base_model import db


class StandardModel(BaseModel):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def summary(self) -> dict:
        pass
