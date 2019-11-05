from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from api import http_status
from api.errors import ApiException

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ApiException(
                f'Vyskytla sa chyba pri vytvorení záznamu: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )

    def update(self, params: dict):
        try:
            for key, value in params.items():
                setattr(self, key, value)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ApiException(
                f'Vyskytla sa chyba pri upravení záznamu: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )

    def delete(self):
        try:
            setattr(self, 'deleted_at', datetime.now())
            db.session.commit()
        except DatabaseError as e:
            raise ApiException(
                f'Vyskytla sa chyba pri vymazaní záznamu: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )
