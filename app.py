from flask import render_template, jsonify, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from forms import CreateCampaignForm, SearchCampaignForm, LoginForm
from app_init import app, bcrypt
from models import Campaign, User
from db import db
import datetime


def get_icon(d1):
    d2 = datetime.date.today()
    if d1 > d2:
        return "static/didnt_begin.png"
    elif d2 > d1:
        return "static/done.png"
    return "static/in_progress.png"


@app.route('/campaigns_test')
def campaigns_test():
    try:
        campaigns = Campaign.query.all()
        return jsonify([e.serialize() for e in campaigns])
    except Exception as e:
        return str(e)


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('התחברות נכשלה. אנא בדוק את שם המשתמש והסיסמא', 'danger')
    return render_template('/login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/about_org')
@login_required
def about_org():
    return render_template('/about_org.html')


@app.route('/create_campaign', methods=['GET', 'POST'])
@login_required
def create_campaign():
    form = CreateCampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(name=form.name.data,
                            city=form.city.data,
                            start_date=form.start_date.data,
                            goal=form.goal.data)
        flash(f'!קמפיין "{campaign.name}" נוצר בהצלחה', 'success')
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('/create_campaign.html', form=form)


@app.route('/manage_campaign', methods=['GET', 'POST'])
@login_required
def manage_campaign():
    form = SearchCampaignForm()
    # Start with an empty query
    campaigns_query = Campaign.query

    if form.submit():
        # If the user added campaign name, add it to the query
        if form.name.data:
            campaigns_query = campaigns_query.filter(Campaign.name.like('%' + form.name.data + '%'))

        # If the user added city name, add it to the query
        if form.city.data:
            campaigns_query = campaigns_query.filter(Campaign.city == form.city.data)

        # If the user selected status
        if form.status.data:
            today = datetime.date.today()
            if form.status.data == "present":
                campaigns_query = campaigns_query.filter(Campaign.start_date == today)
            elif form.status.data == "past":
                campaigns_query = campaigns_query.filter(Campaign.start_date < today)
            elif form.status.data == "future":
                campaigns_query = campaigns_query.filter(Campaign.start_date > today)
    # Preforming the fetch from the DB now
    return render_template('/manage_campaign.html', campaigns=campaigns_query.all(), get_icon=get_icon, form=form)


@app.route('/manage_campaign/campaign_control_panel/<int:campaign_id>')
@login_required
def campaign_control_panel(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('/campaign_control_panel.html', campaign=campaign)


@app.route('/donation', methods=['GET', 'POST'])
@login_required
def donation():
    # if request.method == 'GET':
    # INSERT INTO DB / MOVE TO PP/bit
    # return render_template('/<---->.html')
    return render_template('/donation.html')


@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    # GET REPORTS FROM DB
    return render_template('/reports.html')


@app.route('/create_report', methods=['GET', 'POST'])
@login_required
def create_report():
    # if request.method == 'GET':
    # INSERT INTO DB
    # return redirect(url_for('create_report'))
    return render_template('/create_report.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
