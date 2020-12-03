from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField


class DeviceDatapointPutForm(FlaskForm):
    name = StringField('name')
    code = StringField('code')
    description = StringField('description')
    writable = BooleanField('writable')
    virtual = BooleanField('virtual')
    value = StringField('value')
