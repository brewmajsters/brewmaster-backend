from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, UUID


class ModuleSetValueForm(FlaskForm):
    device_id = StringField(
        'device_id', validators=[
            DataRequired(message='Hodnota device_id je povinná.'),
            UUID(message='Hodnota nie je vo formáte UUID.')
        ]
    )
    datapoint = "ANGLE"  # StringField('data_point', validators=[DataRequired(message='Hodnota datapoint je povinná.')])
    value = IntegerField('value')  # StringField('value', validators=[DataRequired(message='Hodnota value je povinná.')])
