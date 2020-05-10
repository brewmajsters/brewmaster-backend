from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, UUID


class ModuleSetConfigForm(FlaskForm):
    device_id = StringField(
        'device_id', validators=[
            DataRequired(message='Hodnota device_id je povinná.'),
            UUID(message='Hodnota nie je vo formáte UUID.')
        ]
    )
    address = StringField('address', validators=[DataRequired(message='Hodnota address je povinná.')])
    poll_rate = StringField('poll_rate', validators=[DataRequired(message='Hodnota poll_rate je povinná.')])
