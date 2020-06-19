from flask import render_template, jsonify, flash, redirect, url_for, request, session, abort, send_file
from flask_login import login_user, current_user, logout_user, login_required

from neural_network_runner import DEFAULT_NETWORK
from neural_network_runner.cache_manager import set_network_cache, update_network_code
from forms import CreateCampaignForm, SearchCampaignForm, LoginForm, AddNeighborhood, DonationForm, PaperInvoiceForm, \
    DigitalInvoiceForm, BitForm, ReportForm, SearchReportForm, RespondReportForm, validate_name, TeamForm
from app_init import app, bcrypt
from models import Campaign, User, Neighborhood, Team, Donation, Invoice, Building, Report, Notification
from db import db
from neural_network_runner.train import train_model
from utils.campaign import get_response_campaign_neighborhoods, create_teams_and_users, export_neighborhood_to_excel, \
    validate_campaign_status
from utils.teams import delete_team_dependencies, get_team_progress
from utils.notifications import update_notification_status_to_read, create_new_notification
from utils.ui_helpers import get_campaign_icon, get_report_status_icon
from utils.app_decorators import admin_access, user_access
from utils.consts import INVOICE_TYPES, HOST_URL, ORGANIZATION_NAME, ESTIMATE_MINUTES_PER_FLOOR
from utils.automate_report import generate_automate_report
from utils.forms_helpers import search_report_categories
from sqlalchemy import func
import utils.green_invoice as gi
import utils.paypal as pp
import datetime
import json

set_network_cache()


@app.context_processor
def inject_content_to_all_routes():
    return dict(HOST_URL=HOST_URL, ORGANIZATION_NAME=ORGANIZATION_NAME)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.is_active:
            return abort(403)
        session['awaiting_notifications'] = {'have_notification': False, 'amount': 0}
        push_notifications_query = Notification.query.filter(Notification.recipient_id == current_user.id).filter(
            Notification.notified == False)
        pending_notifications = push_notifications_query.all()
        if pending_notifications:
            session['awaiting_notifications'] = {'have_notification': True, 'amount': len(pending_notifications)}
            for notification in pending_notifications:
                notification.notified = True
            db.session.commit()
        session['awaiting_notifications']['badge_notifications'] = current_user.get_num_of_new_notifications() or 0


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.route('/')
@app.route('/home')
@login_required
def home():
    progress = {}
    show_welcome_msg = False
    if not current_user.is_admin:
        if not current_user.team.login_before:
            show_welcome_msg = True
            team = current_user.team
            team.login_before = True
            db.session.commit()
        progress = get_team_progress(current_user.team)
    return render_template('/home.html', progress=progress, show_welcome_msg=show_welcome_msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(is_active=True, username=form.username.data).first()
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
    return_url = request.referrer or '/'
    form = CreateCampaignForm()
    if form.validate_on_submit():
        if validate_name(form.name.data):
            campaign = Campaign(name=form.name.data,
                                city=form.city.data,
                                start_date=form.start_date.data,
                                is_active=True,
                                goal=form.goal.data)
            flash(f'!קמפיין "{campaign.name}" נוצר בהצלחה', 'success')
            db.session.add(campaign)
            db.session.commit()
            return redirect(url_for('home'))
        form.name.errors.append('קמפיין בשם הזה כבר קיים, אנא בחר שם אחר.')
    return render_template('/create_campaign.html', form=form, legend="יצירת קמפיין", return_url=return_url)


@app.route('/manage_campaign/campaign_control_panel/<int:campaign_id>/edit_campaign', methods=['GET', 'POST'])
@login_required
@admin_access
def edit_campaign(campaign_id):
    return_url = request.referrer or '/'
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CreateCampaignForm()
    city = campaign.city
    del form.city
    if form.validate_on_submit():
        validate_campaign_status(campaign)
        if validate_name(form.name.data, campaign.name):
            campaign.name = form.name.data
            campaign.start_date = form.start_date.data
            campaign.goal = form.goal.data
            db.session.commit()
            flash('!הקמפיין עודכן בהצלחה', 'success')
            return redirect(url_for('campaign_control_panel', campaign_id=campaign.id))
        form.name.errors.append('קמפיין בשם הזה כבר קיים, אנא בחר שם אחר.')
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.start_date.data = campaign.start_date
        form.goal.data = campaign.goal
    return render_template('/create_campaign.html', form=form, city=city, legend="עריכת קמפיין", return_url=return_url)


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
    return render_template('/manage_campaign.html',
                           campaigns=campaigns_query.order_by(Campaign.start_date.desc()).all(),
                           get_icon=get_campaign_icon,
                           form=form)


@app.route('/campaign/<int:campaign_id>/neighborhoods', methods=['GET', 'POST'])
@login_required
@admin_access
def manage_campaign_neighborhoods(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = AddNeighborhood()

    # Calling `validate` for the specific field due to flask forms not liking dynamic loaded selection field
    if form.is_submitted() and form.neighborhood_id.data and form.number_of_teams.validate(form):
        validate_campaign_status(campaign)
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


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>/team/<int:team_id>', methods=['DELETE'])
@admin_access
@login_required
def delete_team_route(campaign_id, neighborhood_id, team_id):
    # Safe guards
    campaign = Campaign.query.get_or_404(campaign_id)
    Neighborhood.query.get_or_404(neighborhood_id)
    team = Team.query.get_or_404(team_id)

    validate_campaign_status(campaign)

    delete_team_dependencies(team)

    db.session.commit()
    db.session.delete(team)
    db.session.commit()

    return jsonify({'status': 'OK'})


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>/export_user_data', methods=['GET'])
@admin_access
@login_required
def export_user_data(campaign_id, neighborhood_id):
    # Safe guards
    campaign = Campaign.query.get_or_404(campaign_id)
    Neighborhood.query.get_or_404(neighborhood_id)

    validate_campaign_status(campaign)

    users = db.session.query(User).join(Team).join(Campaign).join(Neighborhood).filter(
        Campaign.id == campaign_id).filter(Neighborhood.id == neighborhood_id)

    # Rest the users' passwords before exporting the file
    User.reset_passwords(users)
    db.session.commit()

    excel_data = export_neighborhood_to_excel(campaign_id, neighborhood_id, users)

    return send_file(excel_data, attachment_filename="output.xlsx", as_attachment=True)


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
                           neighborhood_data=neighborhood.serialize(), campaign_id=campaign_id,
                           ESTIMATE_MINUTES_PER_FLOOR=ESTIMATE_MINUTES_PER_FLOOR,
                           neighborhood_id=neighborhood_id, neighborhood_buildings=serialized_neighborhood_buildings)


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>/team', methods=['POST'])
@admin_access
@login_required
def create_new_team_for_route(campaign_id, neighborhood_id):
    # Safe guards
    campaign = Campaign.query.get_or_404(campaign_id)
    Neighborhood.query.get_or_404(neighborhood_id)

    validate_campaign_status(campaign)

    # Create 1 new team
    new_team_user_data = create_teams_and_users(campaign_id, neighborhood_id, 1)[0]
    new_team_data = db.session.query(Team).join(User).filter(
        User.username == new_team_user_data['username']).first().serialize()

    return jsonify({'user': new_team_user_data, 'team': new_team_data})


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>', methods=['DELETE'])
@admin_access
@login_required
def delete_neighborhood(campaign_id, neighborhood_id):
    # Safe guards
    campaign = Campaign.query.get_or_404(campaign_id)
    neighborhood = Neighborhood.query.get_or_404(neighborhood_id)

    validate_campaign_status(campaign)

    for team in neighborhood.teams:
        delete_team_dependencies(team)

    db.session.commit()
    for team in neighborhood.teams:
        db.session.delete(team)
    db.session.commit()

    return jsonify({'status': 'OK'})


@app.route('/campaign/<int:campaign_id>/neighborhoods/<int:neighborhood_id>/routes', methods=['POST'])
@admin_access
@login_required
def upsert_routes(campaign_id, neighborhood_id):
    # Validate the parameters
    campaign = Campaign.query.get_or_404(campaign_id)
    Neighborhood.query.get_or_404(neighborhood_id)
    body = request.get_json()

    validate_campaign_status(campaign)

    for team_id in body.keys():
        team = Team.query.get_or_404(team_id)
        if team.campaign_id != campaign_id:
            # The user wanted to change team for different campaign - blocking the changes
            return jsonify({"message": "Team not found"}), 404

        # Delete all the buildings
        team.buildings = []
        for building_id in body[team_id]:
            # If the building exists, add it to the team
            b = Building.query.get_or_404(building_id)
            team.buildings.append(b)

    db.session.commit()
    return jsonify({"status": "OK"})


@app.route('/manage_campaign/campaign_control_panel/<int:campaign_id>')
@login_required
@admin_access
def campaign_control_panel(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # Get dynamic values for the total teams and donations information:
    donations = db.session.query(func.sum(Donation.amount)).join(Team).filter(
        Team.campaign_id == campaign_id).scalar()
    teams = db.session.query(func.count(Team.id)).filter(Team.campaign_id == campaign_id).scalar()
    total = {'teams': teams, 'donations': donations if donations else 0}
    return render_template('/campaign_control_panel.html', campaign=campaign, total=total)


@app.route('/donation_address', methods=['GET'])
@login_required
@user_access
def donation_address():
    if session.get('current_building_id'):
        session.pop('current_building_id')

    buildings = current_user.team.buildings
    buildings_donations = Donation.query.filter(Donation.building_id.in_(map(lambda b: b.id, buildings)))
    building_ids_with_donations = list(map(lambda d: d.building_id, buildings_donations))
    serialized_buildings = list(map(lambda b: b.serialize(), buildings))

    for building in serialized_buildings:
        building['have_donations'] = building['id'] in building_ids_with_donations

    neighborhood_data = current_user.team.neighborhood.serialize()

    return render_template('/donation_address.html', buildings=serialized_buildings, neighborhood=neighborhood_data)


@app.route('/donation_address/<int:building_id>', methods=['GET'])
@login_required
@user_access
def set_current_building_id(building_id):
    session['current_building_id'] = building_id

    return redirect(url_for('get_donation'))


@app.route('/donation_address/donation', methods=['GET', 'POST'])
@login_required
@user_access
def get_donation():
    if not session.get('current_building_id'):
        redirect(url_for('donation_address'))

    form = DonationForm()
    conn_error = request.args.get('conn_error')
    validate_campaign_status(current_user.team.campaign)
    if form.validate_on_submit():
        session['current_donation'] = {"amount": form.amount.data,
                                       "payment_type": form.payment_type.data,
                                       "team_id": current_user.team_id}
        if form.payment_type.data == 'bit':
            return redirect(url_for('bit_donation'))
        elif form.payment_type.data == 'PayPal':
            # Create a paypal payment and redirect to the authorization process via paypal's api
            try:
                payment = pp.create_payment(form.amount.data,
                                            f'{HOST_URL}donation_address/donation/paypal/execute_paypal_donation',
                                            f'{HOST_URL}donation_address/donation')
                return redirect(pp.authorize_payment(payment))
            except (ConnectionError, RuntimeError):
                conn_error = True  # if there's a connection error / unexpected error, display an error in the donation page
                generate_automate_report('paypal')
        if not conn_error:
            return redirect(url_for('send_invoice'))
    return render_template('/donation.html', form=form, conn_error=conn_error)


@app.route('/donation_address/donation/bit', methods=['GET', 'POST'])
@login_required
@user_access
def bit_donation():
    if not session.get('current_building_id'):
        redirect(url_for('donation_address'))

    form = BitForm()
    if form.validate_on_submit():
        validate_campaign_status(current_user.team.campaign)
        session['current_donation']['transaction_id'] = form.transaction_id.data
        session.modified = True
        return redirect(url_for('send_invoice'))
    return render_template('/bit_donation.html', form=form)


@app.route('/donation_address/donation/paypal/execute_paypal_donation', methods=['GET', 'POST'])
@login_required
@user_access
def pp_execute():
    """ This route gets the payment authorization and execute the transaction itself via paypal's api """
    validate_campaign_status(current_user.team.campaign)

    pp_req = request.args.to_dict()
    if pp.execute_payment(pp_req):
        session['current_donation']['transaction_id'] = pp_req['paymentId']
        session.modified = True
        return redirect(url_for('send_invoice'))
    return redirect(url_for('get_donation', conn_error=True))


@app.route('/donation_address/donation/invoice', methods=['GET', 'POST'])
@login_required
@user_access
def send_invoice():
    if not session.get('current_building_id'):
        redirect(url_for('donation_address'))

    paper_form = PaperInvoiceForm()
    digital_form = DigitalInvoiceForm()
    conn_error = False  # This way we make sure the conn error will appear only when there's an unexpected error.
    # first we'll check if the forms are validated, so we won't commit the donation with an invoice error.
    if paper_form.submit_p.data and paper_form.validate_on_submit() or \
            digital_form.submit_d.data and digital_form.validate_on_submit():
        validate_campaign_status(current_user.team.campaign)
        # create donation object:
        donation = Donation(amount=session['current_donation']['amount'],
                            payment_type=session['current_donation']['payment_type'],
                            team_id=session['current_donation']['team_id'],
                            transaction_id=session['current_donation'].get('transaction_id'),
                            building_id=session['current_building_id'])
        building = Building.query.get_or_404(session['current_building_id'])

        # checking what kind of invoice was requested, validate It's information and commit it:
        new_invoice = Invoice()
        try:
            if paper_form.submit_p.data:
                new_invoice.reference_id = paper_form.reference_id.data
                new_invoice.type = INVOICE_TYPES['PAPER']
            else:
                clean_address = building.address.split(",")[0].strip()
                clean_city = building.address.split(",")[1].strip()
                # Try to create a client in Green Invoice API and send the invoice to the client
                token = gi.get_bearer_token()
                client_id = gi.create_new_client(token, digital_form.donor_name.data,
                                                 digital_form.mail_address.data, digital_form.donor_id.data,
                                                 address=clean_address, city=clean_city)
                reference_id = gi.send_invoice(token, digital_form.mail_address.data, client_id, donation.amount,
                                               donation.payment_type)
                new_invoice.type = INVOICE_TYPES['DIGITAL']
                new_invoice.reference_id = reference_id
        except (ConnectionError, RuntimeError):
            conn_error = True  # if there's a connection error or unexpected error, display an error in the invoice page
            generate_automate_report('invoice')
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
    if session.get('current_donation'):
        session.pop('current_donation')
    return render_template('/donation_end.html')


@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    form = SearchReportForm()
    # Start with an empty query
    reports_query = Report.query

    # If the user is a team, show only reports from the team's campaign
    if not current_user.is_admin:
        reports_query = reports_query.join(Report.team, aliased=True).filter_by(
            campaign_id=current_user.team.campaign_id)

    if form.submit():
        # If the user is an admin and he chose a specific campaign to show
        if form.campaign.data:
            reports_query = reports_query.join(Report.team, aliased=True).filter_by(
                campaign_id=form.campaign.data)

        # If the user added category, add it to the query
        if form.category.data:
            reports_query = reports_query.filter(Report.category == form.category.data)

        # If the user selected a status
        if form.status.data:
            if form.status.data == "open":
                reports_query = reports_query.filter(Report.is_open)
            elif form.status.data == "closed":
                reports_query = reports_query.filter(Report.is_open == False)  # 'is false' or 'not' are not working.

    # Preforming the fetch from the DB now
    return render_template('/reports.html', reports=reports_query.order_by(Report.creation_time.desc()).all(),
                           get_icon=get_report_status_icon, form=form)


@app.route('/reports/quick', methods=['POST'])
@login_required
def save_quick_report():
    body = request.get_json()
    report = Report(address=body.get('address'),
                    category='דיווח מהיר',
                    description=body.get('transcript'))
    if current_user.team_id:
        report.team_id = current_user.team_id
    db.session.add(report)
    db.session.commit()
    if not current_user.is_admin:
        create_new_notification(1, report)
    return jsonify({'id': report.id})


@app.route('/reports/create_report', methods=['GET', 'POST'])
@login_required
def create_report():
    return_url = request.referrer or '/'
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(category=form.category.data,
                        description=form.description.data,
                        address=form.address.data)
        if current_user.team_id:
            report.team_id = current_user.team_id
        db.session.add(report)
        db.session.commit()
        if not current_user.is_admin:
            create_new_notification(1, report)
        flash('!הדיווח נוצר בהצלחה', 'success')
        return redirect(url_for('reports'))
    return render_template('/create_report.html', form=form, legend="יצירת דיווח", return_url=return_url)


@app.route('/reports/view_report/<int:report_id>')
@login_required
def view_report(report_id):
    report = Report.query.get_or_404(report_id)
    return_url = request.referrer or '/'
    if return_url.endswith(('edit', 'respond', 'close')):
        return_url = url_for('reports')
    return render_template('/view_report.html', report=report, return_url=return_url)


@app.route('/reports/view_report/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    return_url = request.referrer or '/'
    report = Report.query.get_or_404(report_id)
    if report.team_id != current_user.team_id and not current_user.is_admin:
        abort(403)
    form = ReportForm()

    # Quick fix for editing quick reports while It's not a valid option on a normal report:
    if report.category == "דיווח מהיר":
        form.category.render_kw = {'disabled': ""}
        form.category.choices = [(value, value) for value in search_report_categories]
        form.category.data = "דיווח מהיר"
    if form.validate_on_submit():
        report.address = form.address.data
        report.category = form.category.data
        report.description = form.description.data
        db.session.commit()
        flash('!הדיווח עודכן בהצלחה', 'success')
        return redirect(url_for('view_report', report_id=report.id))
    elif request.method == 'GET':
        form.address.data = report.address
        form.category.data = report.category
        form.description.data = report.description
    return render_template('/create_report.html', form=form, legend="עריכת דיווח", return_url=return_url)


@app.route('/reports/view_report/<int:report_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.team_id != current_user.team_id and not current_user.is_admin:
        abort(403)
    for notification in report.notification:
        db.session.delete(notification)
    db.session.delete(report)
    db.session.commit()
    flash('!הדיווח נמחק בהצלחה', 'success')
    return redirect(url_for('reports'))


@app.route('/reports/view_report/<int:report_id>/close', methods=['GET', 'POST'])
@login_required
@admin_access
def close_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.team_id and not current_user.is_admin:
        abort(403)
    report.is_open = False
    report.response = 'לא רלוונטי, נסגר.'
    report.response_time = datetime.datetime.utcnow()
    db.session.commit()
    flash('!הדיווח נסגר בהצלחה', 'success')
    return redirect(url_for('view_report', report_id=report_id))


@app.route('/reports/view_report/<int:report_id>/respond', methods=['GET', 'POST'])
@login_required
@admin_access
def respond_to_report(report_id):
    return_url = request.referrer or '/'
    report = Report.query.get_or_404(report_id)
    if not report.is_open:
        return redirect(url_for('edit_respond', report_id=report.id))
    form = RespondReportForm()
    if form.validate_on_submit():
        report.is_open = False
        report.response = form.response.data
        report.response_time = datetime.datetime.utcnow()
        create_new_notification(report.team.users[0].id, report, 'הדיווח שהזנתם קיבל מענה מהאחראי')
        flash('!הדיווח נענה בהצלחה', 'success')
        return redirect(url_for('reports'))
    return render_template('/report_response.html', report=report, form=form, legend="מענה לדיווח",
                           return_url=return_url)


@app.route('/reports/view_report/<int:report_id>/edit_response', methods=['GET', 'POST'])
@login_required
@admin_access
def edit_response(report_id):
    return_url = request.referrer or '/'
    report = Report.query.get_or_404(report_id)
    if not report.response:
        abort(403)
    form = RespondReportForm()
    if form.validate_on_submit():
        report.response = form.response.data
        report.response_time = datetime.datetime.utcnow()
        notification = Notification(recipient_id=report.team.users[0].id,
                                    description='המענה לדיווח עודכן ע"י האחראי',
                                    report_id=report.id)
        db.session.add(notification)
        db.session.commit()
        flash('!המענה לדיווח עודכן בהצלחה', 'success')
        return redirect(url_for('view_report', report_id=report.id))
    elif request.method == 'GET':
        form.response.data = report.response
    return render_template('/report_response.html', report=report, form=form, legend="עריכת מענה",
                           return_url=return_url)


@app.route('/team/<int:team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.query.get_or_404(team_id)
    progress = get_team_progress(team)
    return render_template('/view_team.html', team=team, progress=progress)


@app.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    if not current_user.is_admin and not current_user.team_id == team_id:
        abort(403)
    team = Team.query.get_or_404(team_id)
    form = TeamForm()
    if form.validate_on_submit():
        team.name = form.name.data
        team.first_teammate_name = form.first_teammate_name.data
        team.second_teammate_name = form.second_teammate_name.data
        db.session.commit()
        flash('!פרטי הצוות עודכנו בהצלחה', 'success')
        return redirect(url_for('view_team', team_id=team.id))
    elif request.method == 'GET':
        form.name.data = team.name
        form.first_teammate_name.data = team.first_teammate_name
        form.second_teammate_name.data = team.second_teammate_name
    return render_template('/edit_team.html', form=form, team_id=team_id)


@app.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():
    campaign_id = request.args.get('campaign_id', None)
    team_query = Team.query
    current_team_money = 0
    neighborhoods_earnings = {}

    # USE CASE 1: USER = TEAM => show only teams within the same campaign and neighborhood
    if not current_user.is_admin:
        team_query = team_query.filter(
            Team.campaign_id == current_user.team.campaign_id and Team.neighborhood_id == current_user.team.neighborhood_id)

    # USE CASE 2: USER = ADMIN => SPECIFIC CAMPAIGN => show only teams within the specific campaign
    elif campaign_id:
        team_query = team_query.filter(Team.campaign_id == campaign_id)

    # USE CASE 3: USER = ADMIN => ALL CAMPAIGNS => query all teams to a dict
    campaign_teams = [t.__dict__ for t in team_query.all()]

    # Calculate total earned money for each team on the leaderboard and insert to the teams dict
    for team in campaign_teams:
        total_earnings = db.session.query(func.sum(Donation.amount)).join(Team).filter(
            Team.id == team['id']).scalar()
        team['total_earnings'] = total_earnings or 0
        # Get the current team earnings to display on the top of the page.
        if not current_user.is_admin and current_user.team_id == team['id']:
            current_team_money = team['total_earnings']

        # If the user has a graph (admin), get neighborhood's earnings information for the graph.
        if current_user.is_admin:
            neighborhood_name = Neighborhood.query.get(team['neighborhood_id']).name
            if neighborhoods_earnings.get(neighborhood_name):
                neighborhoods_earnings[neighborhood_name] += team['total_earnings']
            else:
                neighborhoods_earnings[neighborhood_name] = team['total_earnings']
    campaign_teams = sorted(campaign_teams, key=lambda k: k['total_earnings'], reverse=True)

    # Create the list for the graph information.
    neighborhoods_graph_info = [['שכונה', 'סכום שנאסף']]
    if current_user.is_admin:
        for key, value in neighborhoods_earnings.items():
            neighborhoods_graph_info.append([key, value])

    return render_template('/leaderboard.html', teams=campaign_teams, current_team_money=current_team_money,
                           neighborhoods_graph_info=neighborhoods_graph_info)


@app.route('/notifications')
@login_required
def notifications():
    # Query all the user notifications
    notifications_query = Notification.query.filter(Notification.recipient_id == current_user.id).order_by(
        Notification.creation_date.desc()).all()
    notification_list = []
    for notification in notifications_query:
        notification_list.append(
            {'notification_details_obj': notification,
             'status_icon': get_report_status_icon(not notification.was_read)})
    update_notification_status_to_read()
    return render_template('/notifications.html', notifications=notification_list)


@app.route('/campaign/<int:campaign_id>/close', methods=['GET'])
@admin_access
@login_required
def close_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if not campaign.is_active:
        return abort(403)

    try:
        train_model(campaign_id)
        campaign.is_active = False

        campaign_users = db.session.query(User).join(Team).filter(Team.campaign_id == campaign_id).all()
        for user in campaign_users:
            user.is_active = False

        db.session.commit()
    except:
        flash('אימון המודל נכשל, אנה נסה שנית', 'danger')
    finally:
        return redirect(url_for("campaign_control_panel", campaign_id=campaign_id))


@app.route('/admin/reset_model', methods=['GET'])
@admin_access
@login_required
def reset_model():
    update_network_code(DEFAULT_NETWORK)
    return redirect(request.referrer or '/')


@app.route('/admin/force_train/<int:campaign_id>', methods=['GET'])
@login_required
@admin_access
def force_train(campaign_id):
    Campaign.query.get_or_404(campaign_id)
    train_model(campaign_id)
    return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
