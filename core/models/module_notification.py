import datetime
from core.models.abstract.base_model import db
from core.models.abstract.timescale_model import TimeScaleModel
from sqlalchemy.dialects.postgresql import UUID


class ModuleNotification(TimeScaleModel):
    __tablename__ = 'module_notifications'
    __timestamp_field__ = 'time'

    time = db.Column(db.DateTime, nullable=False, primary_key=True, default=datetime.datetime.utcnow)
    message = db.Column(db.String(250), nullable=False)

    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id'))

    module = db.relationship("Module", back_populates="module_notification")
