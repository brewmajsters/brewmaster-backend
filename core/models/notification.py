from sqlalchemy import types
from core.models.abstract.base_model import db
from core.models.abstract.standard_model import StandardModel


class Notification(StandardModel):
    __tablename__ = 'notification'

    message = db.Column(db.String(100), nullable=True)
    method = db.Column(db.String(10), default='GET')
    url = db.Column(db.String(250), default='/')
    module = db.Column(db.String(50))
    function = db.Column(db.String(50))
    level = db.Column(db.String(50), default='')
    status_code = db.Column(db.Integer, nullable=True)
    request = db.Column(types.JSON(), nullable=True)
    additional_data = db.Column(types.JSON(), nullable=True)

    def __init__(self, message, method, url, module, function, level, status_code, request, additional_data):
        self.message = message
        self.method = method
        self.url = url
        self.module = module
        self.function = function
        self.level = level
        self.status_code = status_code
        self.request = request
        self.additional_data = additional_data
