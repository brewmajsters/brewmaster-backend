from sqlalchemy import DDL, event
from core.models.base_model import db


# class BaseTimeScaleModel():
#     __abstract__ = True
#     __tablename__ = 'sensors'
#     __timestamp_field__ = 'time'
#
#     trigger = DDL(
#         f"SELECT create_hypertable('{__tablename__}', '{__timestamp_field__}');"
#     )
#
#     event.listen(
#         __tablename__,
#         'after_create',
#         trigger.execute_if(dialect='postgresql')
#     )
