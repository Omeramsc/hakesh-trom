from flask import render_template, jsonify, flash, redirect, url_for, request, session
from flask_login import login_user, current_user, logout_user, login_required
from forms import CreateCampaignForm, SearchCampaignForm, LoginForm, AddNeighborhood, DonationForm, PaperInvoiceForm, \
    DigitalInvoiceForm, BitForm
from app_init import app, bcrypt
from models import Campaign, User, Neighborhood, Team, Donation, Invoice
from db import db
from utils.forms_helpers import get_campaign_icon
from utils.campaign import get_response_campaign_neighborhoods, create_teams_and_users
from utils.app_decorators import admin_access, user_access
from utils.consts import INVOICE_TYPES
import utils.green_invoice as gi
import datetime
import json


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.route('/admin/campaigns', methods=["GET"])
def campaigns_test():
    try:
        campaigns = Campaign.query.all()
        return jsonify([e.serialize() for e in campaigns])
    except Exception as e:
        return str(e)


@app.route('/admin/campaigns/<int:campaign_id>', methods=["DELETE"])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    for team in campaign.teams:
        for user in team.users:
            db.session.delete(user)
        db.session.delete(team)

    db.session.delete(campaign)
    db.session.commit()
    return '', 204


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
@admin_access
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
@admin_access
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
    return render_template('/manage_campaign.html', campaigns=campaigns_query.all(), get_icon=get_campaign_icon,
                           form=form)


@app.route('/campaign/<int:campaign_id>/neighborhoods', methods=['GET', 'POST'])
@login_required
@admin_access
def manage_campaign_neighborhoods(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = AddNeighborhood()

    # Calling `validate` for the specific field due to flask forms not liking dynamic loaded selection field
    if form.is_submitted() and form.neighborhood_id.data and form.number_of_teams.validate(form):
        teams_users_data = create_teams_and_users(campaign_id, int(form.neighborhood_id.data),
                                                  int(form.number_of_teams.data))
        flash(json.dumps(teams_users_data), 'users_data')
        return redirect(url_for('manage_campaign_neighborhoods', campaign_id=campaign_id))

    # Getting the available and selected neighborhoods
    available_neighborhoods, campaign_neighborhoods = get_response_campaign_neighborhoods(campaign)

    # Building neighborhood selection choices
    form.neighborhood_id.choices = list(map(lambda x: (x['id'], x['name']), available_neighborhoods))
    # Set default number of teams
    form.number_of_teams.process_data(1)

    return render_template('/campaign_neighborhoods_selection.html', campaign_neighborhoods=campaign_neighborhoods,
                           form=form, campaign_id=campaign_id, loads_json=json.loads)


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>', methods=['GET', 'POST'])
@admin_access
@login_required
def manage_neighborhood_route(campaign_id, neighborhood_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    neighborhood = Neighborhood.query.get_or_404(neighborhood_id)
    neighborhood_buildings = neighborhood.buildings
    neighborhood_teams = Team.query.filter_by(campaign_id=campaign.id, neighborhood_id=neighborhood.id).all()

    serialized_neighborhood_teams = list(map(lambda team: team.serialize(), neighborhood_teams))
    serialized_neighborhood_buildings = list(map(lambda building: building.serialize(), neighborhood_buildings))

    return render_template('/neighborhood_route_builder.html', neighborhood_teams=serialized_neighborhood_teams,
                           neighborhood_data=neighborhood.serialize(),
                           neighborhood_buildings=serialized_neighborhood_buildings)


@app.route('/manage_campaign/campaign_control_panel/<int:campaign_id>')
@login_required
@admin_access
def campaign_control_panel(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('/campaign_control_panel.html', campaign=campaign)


@app.route('/donation_address', methods=['GET', 'POST'])
@login_required
@user_access
def donation_address():
    return render_template('/donation_address.html')


@app.route('/donation_address/donation', methods=['GET', 'POST'])
@login_required
@user_access
def get_donation():
    form = DonationForm()
    if form.validate_on_submit():
        session['current_donation'] = {"amount": form.amount.data,
                                       "payment_type": form.payment_type.data,
                                       "team_id": current_user.team_id}
        if form.payment_type.data == 'bit':
            return redirect(url_for('bit_donation'))
        return redirect(url_for('send_invoice'))
        # FOR NOW, IGNORE PAYPAL AND BIT AND APPLY CASH DONATIONS FLOW ONLY
    return render_template('/donation.html', form=form)


@app.route('/donation_address/donation/bit', methods=['GET', 'POST'])
@login_required
@user_access
def bit_donation():
    form = BitForm()
    if form.validate_on_submit():
        session['current_donation']['transaction_id'] = form.transaction_id.data
        return redirect(url_for('send_invoice'))
    return render_template('/bit_donation.html', form=form)


@app.route('/donation_address/donation/invoice', methods=['GET', 'POST'])
@login_required
@user_access
def send_invoice():
    paper_form = PaperInvoiceForm()
    digital_form = DigitalInvoiceForm()
    conn_error = False  # This way we make sure the conn error will appear only when there's an unexpected error.

    # first we'll check if the forms are validated, so we won't commit the donation with an invoice error.
    if paper_form.submit_p.data and paper_form.validate_on_submit() or \
            digital_form.submit_d.data and digital_form.validate_on_submit():

        # create donation object:
        donation = Donation(amount=session['current_donation']['amount'],
                            payment_type=session['current_donation']['payment_type'],
                            team_id=session['current_donation']['team_id'],
                            transaction_id=session['current_donation'].get('transaction_id'))

        # checking what kind of invoice was requested, validate It's information and commit it:
        new_invoice = Invoice()
        try:
            if paper_form.submit_p.data:
                new_invoice.reference_id = paper_form.reference_id.data
                new_invoice.type = INVOICE_TYPES['PAPER']
            else:

                # Try to create a client in Green Invoice API and send the invoice to the client
                token = gi.get_bearer_token()
                client_id = gi.create_new_client(token, digital_form.donor_name.data,
                                                 digital_form.mail_address.data, digital_form.donor_id.data)
                reference_id = gi.send_invoice(token, digital_form.mail_address.data, client_id, donation.amount,
                                               donation.payment_type)
                new_invoice.type = INVOICE_TYPES['DIGITAL']
                new_invoice.reference_id = reference_id
        except (ConnectionError, RuntimeError):
            conn_error = True  # if there's a connection error or unexpected error, display an error in the invoice page
        except ValueError:
            digital_form.donor_id.errors.append("מספר ת.ז אינו תקין")
        else:

            # If all went well, commit the donation.
            db.session.add(donation)
            db.session.commit()

            # after we committed the donation, we get it's id for the invoice FK and commit the invoice.
            new_invoice.donation_id = donation.id
            db.session.add(new_invoice)
            db.session.commit()
            return redirect(url_for('donation_end'))
    return render_template('/invoice.html', paper_form=paper_form, digital_form=digital_form, conn_error=conn_error)


@app.route('/donation_address/donation/invoice/thanks')
@login_required
@user_access
def donation_end():
    if session['current_donation']:
        session.pop('current_donation')
    return render_template('/donation_end.html')


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
