from sqlalchemy import DDL, event
from core.models.base_model import db


class BaseTimeScaleModel(db.Model):
    __abstract__ = True
    __tablename__ = None

    trigger = DDL(
        f"CREATE TRIGGER dt_ins BEFORE INSERT ON {__tablename__} "
        "FOR EACH ROW BEGIN SET NEW.data='ins'; END"
    )

    event.listen(
        __tablename__,
        'after_create',
        trigger.execute_if(dialect='postgresql')
    )
