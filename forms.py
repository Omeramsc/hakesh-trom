from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Length


class CreateCampaignForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(), Length(min=3, max=50)])
    city = StringField('city', validators=[DataRequired(), Length(min=1, max=50)])
    start_date = DateField('start_date')
    goal = FloatField('goal')

    submit = SubmitField('צור קמפיין')
