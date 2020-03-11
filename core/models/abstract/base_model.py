from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from api import http_status
from api.errors import ApiException

db = SQLAlchemy()


def initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    def get(self, **kwargs):
        try:
            return self.query().filter_by(**kwargs).first()
        except MultipleResultsFound as e:
            raise ApiException(
                f'Multiple results found.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )
        except NoResultFound as e:
            raise ApiException(
                f'No result found.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ApiException(
                f'There was an error creating the record: {self}.',
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
                f'There was an error updating the record: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )

    def delete(self):
        try:
            setattr(self, 'deleted_at', datetime.now())
            db.session.commit()
        except DatabaseError as e:
            raise ApiException(
                f'There was an error deleting the record: {self}.',
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                previous=e
            )
