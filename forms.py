from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Campaign
import json


def read_cities():
    with open('static/israel-cities.json', 'r', encoding="utf8") as data:
        data = json.load(data)
    for line in data:
        if ")" not in line.get('name'):
            yield line.get('name')


def get_cities():
    cities = [(['תל - אביב - יפו', 'תל אביב - יפו'])]
    for city in read_cities():
        cities.append(tuple([city, city]))
    return cities


class CreateCampaignForm(FlaskForm):
    name = StringField('*שם הקמפיין:',
                       validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "הכנס שם לקמפיין"})
    start_date = DateField('*תאריך:', validators=[DataRequired()], format='%Y-%m-%d')
    goal = FloatField('ייעד כספי', render_kw={"placeholder": "הכנס יעד"})
    city = SelectField('*עיר:', choices=get_cities(), validators=[DataRequired()])

    submit = SubmitField('צור קמפיין')

    def validate_name(self, name):
        campaign_name = Campaign.query.filter_by(name=name.data).first()
        if campaign_name:
            raise ValidationError('קמפיין בשם הזה כבר קיים, אנא בחר שם אחר.')
