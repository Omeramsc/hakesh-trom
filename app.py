from flask import render_template, jsonify, flash, redirect, url_for
from app_init import app
from forms import CreateCampaignForm, SearchCampaignForm
from models import Campaign
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
def home():
    return render_template('/index.html')


@app.route('/about_org')
def about_org():
    return render_template('/about_org.html')


@app.route('/create_campaign', methods=['GET', 'POST'])
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
def manage_campaign():
    form = SearchCampaignForm()
    campaigns = Campaign.query.all()
    if form.submit():
        if form.name.data:
            if form.city.data:
                campaigns = Campaign.query.filter(Campaign.name.like('%' + form.name.data + '%'),
                                                  Campaign.city == form.city.data).all()
            else:
                campaigns = Campaign.query.filter(Campaign.name.like('%' + form.name.data + '%')).all()
        elif form.city.data:
            campaigns = Campaign.query.filter(Campaign.city == form.city.data).all()
        elif form.status.data:  # For some reason, this statement never works. it is always true. and so,
            # It's impossible to clear selection.
            today = datetime.date.today()
            if form.status.data == "present":
                campaigns = Campaign.query.filter(Campaign.start_date == today)
            elif form.status.data == "past":
                campaigns = Campaign.query.filter(Campaign.start_date < today)
            elif form.status.data == "future":
                campaigns = Campaign.query.filter(Campaign.start_date > today)

    return render_template('/manage_campaign.html', campaigns=campaigns, func=get_icon, form=form)


@app.route('/manage_campaign/campaign_control_panel/<int:campaign_id>')
def campaign_control_panel(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('/campaign_control_panel.html')


@app.route('/donation', methods=['GET', 'POST'])
def donation():
    # if request.method == 'GET':
    # INSERT INTO DB / MOVE TO PP/bit
    # return render_template('/<---->.html')
    return render_template('/donation.html')


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    # GET REPORTS FROM DB
    return render_template('/reports.html')


@app.route('/create_report', methods=['GET', 'POST'])
def create_report():
    # if request.method == 'GET':
    # INSERT INTO DB
    # return redirect(url_for('create_report'))
    return render_template('/create_report.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
