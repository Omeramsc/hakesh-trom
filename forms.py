from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, RadioField, PasswordField, BooleanField, \
    IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, Email, Regexp
from models import Campaign
from utils.consts import INVOICE_REF_LENGTH, BIT_ACCOUNT_NUM
from utils.forms_helpers import report_categories, read_cities


def validate_name(name, current_name=None):
    if not current_name or name != current_name:  # run the validation only if It's a new campaign, or the name changed
        campaign = Campaign.query.filter_by(name=name).first()
        if campaign:
            return False
    return True


class CreateCampaignForm(FlaskForm):
    name = StringField('*שם הקמפיין:',
                       validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                   Length(min=3, max=50, message='על שם הקמפיין להכיל בין 3 ל-50 תווים')],
                       render_kw={"placeholder": "הכנס שם לקמפיין"})
    start_date = DateField('*תאריך:', validators=[DataRequired(message='שדה זה הינו שדה חובה')], format='%Y-%m-%d')
    goal = IntegerField('ייעד כספי', render_kw={"placeholder": "הכנס יעד", "value": 0})
    city = SelectField('*עיר:', choices=read_cities(), validators=[DataRequired(message='שדה זה הינו שדה חובה')])

    submit = SubmitField('שמור קמפיין')


class SearchCampaignForm(FlaskForm):
    name = StringField('שם הקמפיין:', render_kw={"placeholder": "הכנס את שם הקמפיין"})
    city = SelectField('עיר:', choices=[("", "בחר עיר")] + read_cities(), default="")
    status = RadioField(choices=[("all", "הכל"), ("past", "הסתיים"), ("present", "מתרחש"), ("future", "עתידי")],
                        default="all")

    submit = SubmitField('בצע חיפוש')


class LoginForm(FlaskForm):
    username = StringField('שם משתמש:',
                           validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                       Length(min=2, max=20, message='על שם המשתמש להכיל בין 2 ל-20 תווים')],
                           render_kw={"placeholder": "הזן שם משתמש"})
    password = PasswordField('סיסמא:', validators=[DataRequired(message='שדה זה הינו שדה חובה')],
                             render_kw={"placeholder": "הזן סיסמא"})
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')


class AddNeighborhood(FlaskForm):
    neighborhood_id = SelectField("בחר שכונה", coerce=int, validators=[DataRequired(message='שדה זה הינו שדה חובה')],
                                  choices=[])
    number_of_teams = IntegerField("מספר צוותים", validators=[NumberRange(min=1)])
    submit = SubmitField('הוסף שכונה')


class DonationForm(FlaskForm):
    amount = FloatField('סכום לתרומה:', validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                                    NumberRange(min=5, message='אין להזין תרומות '
                                                                               'מתחת ל-5 ש"ח')])
    payment_type = RadioField('אמצעי תשלום', validators=[DataRequired(message="סוג התשלום הינו שדה חובה")],
                              choices=[("PayPal", 'PayPal'), ("Cash", 'מזומן'), ("bit", 'bit')], default="Cash")
    submit = SubmitField('המשך')


class BitForm(FlaskForm):
    account_num = StringField("מספר איש קשר להעברה:", render_kw={"value": BIT_ACCOUNT_NUM, "disabled": ""})
    transaction_id = StringField('מספר אישור:', validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                                            Regexp('^[0-9]{4}-[0-9]{4}-[0-9]{5}$',
                                                                   message='אנא הזן את מספר האישור '
                                                                           'לפי ההנחיה')])
    submit = SubmitField('המשך')


class PaperInvoiceForm(FlaskForm):
    reference_id = StringField('מספר קבלה:',
                               validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                           Length(min=INVOICE_REF_LENGTH, max=INVOICE_REF_LENGTH,
                                                  message=f'אנא הזן את מספר הקבלה הכולל {INVOICE_REF_LENGTH} ספרות '
                                                          f'במלואו')])
    submit_p = SubmitField('סיים תרומה')


class DigitalInvoiceForm(FlaskForm):
    mail_address = StringField('כתובת מייל:', validators=[DataRequired(message='שדה זה הינו שדה חובה'),
                                                          Email(message='אנא הזן כתובת מייל תקינה')])
    donor_id = StringField('ת.ז/ח.פ התורם:',
                           validators=[DataRequired(message='שדה זה הינו שדה חובה'), Length(min=9, max=9,
                                                                                            message='אנא הזן מספר '
                                                                                                    'ת.ז/ח.פ בעל 9 '
                                                                                                    'ספרות, '
                                                                                                    'כולל ספרת '
                                                                                                    'הביקורת')])
    donor_name = StringField('שם התורם:', validators=[DataRequired(message='שדה זה הינו שדה חובה')])

    submit_d = SubmitField('סיים תרומה')


class ReportForm(FlaskForm):
    address = StringField('כתובת:', validators=[DataRequired(message='שדה זה הינו שדה חובה')],
                          render_kw={"placeholder": "הזן את כתובת המיקום של האירוע"})
    category = SelectField('סוג הדיווח:', choices=[(value, value) for value in report_categories],
                           validators=[DataRequired(message='שדה זה הינו שדה חובה')])
    description = TextAreaField('תיאור:', validators=[DataRequired(message='שדה זה הינו שדה חובה'), Length(max=200,
                                                                                                           message='אנא הזן תיאור עד 200 תווים.')])

    submit = SubmitField('שמור דיווח')


class RespondReportForm(FlaskForm):
    response = TextAreaField('תשובה:', validators=[DataRequired(message='שדה זה הינו שדה חובה'), Length(max=200,
                                                                                                        message='אנא הזן תיאור עד 200 תווים.')],
                             default="קיבלתי, תודה.")

    submit = SubmitField('שמור מענה')


class SearchReportForm(FlaskForm):
    category = SelectField('סוג הדיווח:', choices=[(value, value) for value in report_categories], default="")
    status = RadioField(choices=[("all", "הכל"), ("open", "פתוח"), ("closed", "סגור")], default="all")
    submit = SubmitField('בצע חיפוש')
