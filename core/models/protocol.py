from sqlalchemy.dialects.postgresql import UUID
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Protocol(StandardModel):
    __tablename__ = 'protocols'

    name = db.Column(db.String(100), nullable=True)
    datatype_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_types.id'))

    module_device_types = db.relationship("ModuleDeviceType", back_populates="protocol")
    datatype = db.relationship("DataType", back_populates="protocols")

    def summary(self) -> dict:
        return dict(
            id=str(self.id),
            datatype_id=str(self.datatype_id),
            name=self.name,
        )
