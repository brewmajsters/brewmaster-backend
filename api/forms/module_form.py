from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, UUID


class ModuleSetValueForm(FlaskForm):
    device_id = StringField(
        'device_id', validators=[
            DataRequired(message='Hodnota device_id je povinná.'),
            UUID(message='Hodnota nie je vo formáte UUID.')
        ]
    )
    data_point = StringField('data_point', validators=[DataRequired(message='Hodnota data_point je povinná.')])
    value = StringField('value', validators=[DataRequired(message='Hodnota value je povinná.')])
