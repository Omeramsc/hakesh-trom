from flask import render_template, jsonify, flash, redirect, url_for
from app_init import app
from forms import CreateCampaignForm
from models import Campaign
from db import db


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


@app.route('/first_steps')
def first_steps():
    return render_template('/first_steps.html')


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


@app.route('/manage_campaign')
def manage_campaign():
    return render_template('/manage_campaign.html')


@app.route('/manage_campaign/campaign_control_panel')
def campaign_control_panel():
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
