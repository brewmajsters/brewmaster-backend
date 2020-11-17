from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeviceDatapointSetValueForm(FlaskForm):
    value = StringField('value', validators=[DataRequired(message='Hodnota value je povinná.')])
