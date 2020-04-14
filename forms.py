from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, RadioField, PasswordField, BooleanField, \
    IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, Email
from models import Campaign
import json


def memoize_dropdown(func):
    """Checks if the dropdown list has already been created.
    If it did, it returns the cached list. otherwise, it creates one.
    """

    dropdown_cache = []

    def wrapper():
        if not dropdown_cache:
            for city in func():
                dropdown_cache.append((city, city))
        return dropdown_cache

    return wrapper


@memoize_dropdown
def read_cities():
    """Reads the city-list files, while putting 'Tel-Aviv' first and ignoring tribes & settlement."""
    with open('static/israel-cities.json', 'r', encoding="utf8") as data:
        data = json.load(data)
    yield 'תל - אביב - יפו'
    for line in data:
        if ")" not in line.get('name'):
            yield line.get('name')


class CreateCampaignForm(FlaskForm):
    name = StringField('*שם הקמפיין:',
                       validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "הכנס שם לקמפיין"})
    start_date = DateField('*תאריך:', validators=[DataRequired()], format='%Y-%m-%d')
    goal = FloatField('ייעד כספי', render_kw={"placeholder": "הכנס יעד"})
    city = SelectField('*עיר:', choices=read_cities(), validators=[DataRequired()])

    submit = SubmitField('צור קמפיין')

    def validate_name(self, name):
        campaign_name = Campaign.query.filter_by(name=name.data).first()
        if campaign_name:
            raise ValidationError('קמפיין בשם הזה כבר קיים, אנא בחר שם אחר.')


class SearchCampaignForm(FlaskForm):
    name = StringField('שם הקמפיין:', render_kw={"placeholder": "הכנס את שם הקמפיין"})
    city = SelectField('עיר:', choices=[("", "בחר עיר")] + read_cities(), default="")
    status = RadioField(choices=[("past", 'הסתיים'), ("present", 'מתרחש'), ("future", 'עתידי')])

    submit = SubmitField('בצע חיפוש')


class LoginForm(FlaskForm):
    username = StringField('שם משתמש:', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "הזן שם משתמש"})
    password = PasswordField('סיסמא:', validators=[DataRequired()], render_kw={"placeholder": "הזן סיסמא"})
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')


class AddNeighborhood(FlaskForm):
    neighborhood_id = SelectField("בחר שכונה", coerce=int, validators=[DataRequired()], choices=[])
    number_of_teams = IntegerField("מספר צוותים", validators=[NumberRange(min=1)])
    submit = SubmitField('הוסף שכונה')


class DonationForm(FlaskForm):
    amount = FloatField('סכום לתרומה:', validators=[DataRequired(), NumberRange(min=5, message='*אין להזין תרומות '
                                                                                               'מתחת ל-5 ש"ח')])
    payment_type = RadioField('אמצעי תשלום', validators=[DataRequired(message="*סוג התשלום הינו שדה חובה")],
                              choices=[("PayPal", 'PayPal'), ("Cash", 'מזומן'), ("bit", 'bit')], default="Cash")
    submit = SubmitField('המשך')


class PaperInvoiceForm(FlaskForm):
    reference_id = IntegerField('מספר קבלה:',
                                validators=[DataRequired()])
    submit_p = SubmitField('סיים תרומה')


class DigitalInvoiceForm(FlaskForm):
    mail_address = StringField('כתובת מייל למשלוח הקבלה:', validators=[DataRequired(), Email])
    donor_id = IntegerField('ת.ז התורם:', validators=[DataRequired()])
    donor_name = StringField('שם התורם:',  validators=[DataRequired()])

    submit_d = SubmitField('סיים תרומה')
