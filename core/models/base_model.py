from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except DatabaseError as err:
            db.session.rollback()
            raise err
