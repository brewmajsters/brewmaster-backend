from sqlalchemy import DDL, event
from api import http_status
from api.errors import ApiException
from core.models import BaseModel


class TimeScaleModel(BaseModel):
    __table__ = None
    __abstract__ = True
    __tablename__ = 'abstract'
    __timestamp_field__ = 'time'

    def summary(self) -> dict:
        pass


@event.listens_for(TimeScaleModel, 'instrument_class', propagate=True)
def instrument_class(mapper, class_):
    if mapper.local_table is not None:
        if hasattr(class_, '__timestamp_field__') and class_.__timestamp_field__:
            trigger_for_table(mapper.local_table, class_.__timestamp_field__)
        else:
            raise ApiException(
                'Attribute __timestamp_field_ must be specified.',
                http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def trigger_for_table(table, timestamp):
    trigger = DDL(
        f"SELECT create_hypertable('{table.name}', '{timestamp}');"
    )

    event.listen(table, 'after_create', trigger.execute_if(dialect='postgresql'))
