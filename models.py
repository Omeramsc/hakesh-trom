import datetime

from neural_network_runner import run_network
from db import db
from app_init import login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from utils.consts import DEFAULT_TEAM_USER_PASSWORD, ESTIMATE_MINUTES_PER_FLOOR
from utils.network_input import STANDARDIZE_TYPE_FLOORS, STANDARDIZE_TYPE_EARNINGS, STANDARDIZE_TYPE_HEIGHT, \
    STANDARDIZE_TYPE_NEIGHBORHOOD, encodeInput, decodeInput
from utils.ui_helpers import pretty_time

buildings_teams_association_table = db.Table('buildings_teams', db.Model.metadata,
                                             db.Column('building_id', db.Integer, db.ForeignKey('buildings.id')),
                                             db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
                                             )


class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'))
    neighborhood = db.relationship("Neighborhood", back_populates="buildings")
    attributes = db.Column(JSON)
    geometry = db.Column(JSON)
    center_point = db.Column(JSON)
    address = db.Column(db.String)
    last_campaign_earnings = db.Column(db.Float)
    teams = db.relationship(
        "Team",
        secondary=buildings_teams_association_table,
        back_populates="buildings")
    donations = db.relationship("Donation", back_populates="building")

    def get_encoded_input(self):
        return {
            'ms_komot': encodeInput(self.attributes['ms_komot'], STANDARDIZE_TYPE_FLOORS),
            'gova_simplex_2019': encodeInput(self.attributes['gova_simplex_2019'], STANDARDIZE_TYPE_HEIGHT),
            'max_height': encodeInput(self.attributes['max_height'], STANDARDIZE_TYPE_HEIGHT),
            'min_height': encodeInput(self.attributes['min_height'], STANDARDIZE_TYPE_HEIGHT),
            'neighborhoodName': encodeInput(self.attributes['ms_shchuna'], STANDARDIZE_TYPE_NEIGHBORHOOD),
            'lastYearEarnings': encodeInput(self.last_campaign_earnings, STANDARDIZE_TYPE_EARNINGS),
        }

    def predict_earnings(self):
        encoded_input = self.get_encoded_input()
        encoded_prediction = run_network(encoded_input)['currentYearEarnings']

        return float("{:.2f}".format(decodeInput(encoded_prediction, STANDARDIZE_TYPE_EARNINGS)))

    def serialize(self):
        total_minutes = int(self.attributes.get('ms_komot', 0)) * ESTIMATE_MINUTES_PER_FLOOR
        return {
            'id': self.id,
            'address': self.address,
            'geometry': self.geometry,
            'center_point': self.center_point,
            'last_campaign_earnings': self.last_campaign_earnings,
            'predicted_earnings': self.predict_earnings(),
            'number_of_floors': self.attributes.get('ms_komot', 0),
            'estimated_minutes': total_minutes
        }


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    first_teammate_name = db.Column(db.String, nullable=True)
    second_teammate_name = db.Column(db.String, nullable=True)
    login_before = db.Column(db.Boolean, default=False, nullable=True)
    users = db.relationship("User", back_populates="team")
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    campaign = db.relationship("Campaign", back_populates="teams")
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'))
    neighborhood = db.relationship("Neighborhood", back_populates="teams")
    buildings = db.relationship(
        "Building",
        secondary=buildings_teams_association_table,
        back_populates="teams")
    donations = db.relationship("Donation", back_populates="team")
    reports = db.relationship("Report", back_populates="team")

    def __init__(self, neighborhood_id, campaign_id):
        self.neighborhood_id = neighborhood_id
        self.campaign_id = campaign_id

    def serialize(self):
        serialized_buildings = list(map(lambda building: building.serialize(), self.buildings))
        predicted_total = sum(map(lambda building: building['predicted_earnings'], serialized_buildings))
        total_minutes = sum(
            map(lambda building: int(building['number_of_floors']), serialized_buildings)) * ESTIMATE_MINUTES_PER_FLOOR

        return {
            'id': self.id,
            'buildings': serialized_buildings,
            'predicted_total': float("{:.2f}".format(predicted_total)),
            'pretty_total_minutes': pretty_time(total_minutes)
        }


class Neighborhood(db.Model):
    __tablename__ = 'neighborhoods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city_name = db.Column(db.String, nullable=False)
    geometry = db.Column(JSON)
    teams = db.relationship("Team", back_populates="neighborhood")
    buildings = db.relationship("Building", back_populates="neighborhood")
    center_point = db.Column(JSON)

    def __init__(self, name, city_name, geometry):
        self.name = name
        self.city_name = city_name
        self.geometry = geometry

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'center_point': self.center_point,
            'geometry': self.geometry
        }


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    goal = db.Column(db.Float())
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    teams = db.relationship("Team", back_populates="campaign")
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, city, start_date, goal, is_active):
        self.name = name
        self.city = city
        self.start_date = start_date
        self.goal = goal
        self.is_active = is_active

    def __repr__(self):
        return f'id: {self.id}\nname: {self.name}\ncity: {self.city}\ndate: {self.start_date}\n goal: {self.goal}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'goal': self.goal,
            'start_date': self.start_date,
            'creation_date': self.creation_date
        }

    def get_neighborhoods(self, teams_cache=None):
        teams = self.teams if teams_cache is None else teams_cache

        neighborhood_ids = [team.neighborhood_id for team in teams]
        return Neighborhood.query.filter(Neighborhood.id.in_(neighborhood_ids)).all()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", back_populates="users")
    notifications = db.relationship("Notification", back_populates="recipient")

    def __init__(self, username, password, is_admin=False, is_active=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    @staticmethod
    def reset_passwords(users):
        """
        Reset passwords for a the given list of users
        :param users: list of users
        :return:
        """
        for user in users:
            user.set_password(DEFAULT_TEAM_USER_PASSWORD)

    def get_num_of_new_notifications(self):
        return Notification.query.filter_by(recipient=self).filter(Notification.was_read == False).count()

    def __repr__(self):
        return f'id: {self.id}\nusername: {self.username}\nis_active: {self.is_active}\nis_admin: {self.is_admin}\n ' \
               f'creation_date: {self.creation_date} '

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': 'Admin' if self.is_admin else 'User',
            'creation_date': self.creation_date
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient = db.relationship("User", back_populates="notifications")
    description = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    was_read = db.Column(db.Boolean, default=False, nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    report = db.relationship("Report", back_populates="notification")
    notified = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, recipient_id, description, report_id=None):
        self.recipient_id = recipient_id
        self.description = description
        self.report_id = report_id


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(), nullable=False)
    payment_type = db.Column(db.String(), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", back_populates="donations")
    transaction_id = db.Column(db.String(), nullable=True)
    invoice = db.relationship("Invoice", back_populates="donation")
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    building = db.relationship("Building", back_populates="donations")

    def __init__(self, amount, payment_type, team_id, transaction_id, building_id):
        self.amount = amount
        self.payment_type = payment_type
        self.team_id = team_id
        self.transaction_id = transaction_id
        self.building_id = building_id

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'team_id': self.team_id,
        }


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    reference_id = db.Column(db.String(), nullable=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donations.id'), nullable=False)
    donation = db.relationship("Donation", back_populates="invoice")

    def __init__(self, donation_id=None, type=None, reference_id=None):
        self.donation_id = donation_id
        self.type = type
        self.reference_id = reference_id

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'reference_id': self.reference_id,
            'donation_id': self.donation_id,
        }


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_open = db.Column(db.Boolean, default=True, nullable=False)
    response = db.Column(db.String, nullable=True)
    response_time = db.Column(db.DateTime, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", back_populates="reports")
    notification = db.relationship("Notification", back_populates="report")

    def __init__(self, category, description, address="ללא כתובת"):
        self.address = address
        self.category = category
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'category': self.category,
            'description': self.description,
            'creation_time': self.creation_time,
            'is_open': self.is_open,
            'response': self.response,
            'response_time': self.response_time,
            'team_id': self.team_id,
        }


class NeuralNetwork(db.Model):
    __tablename__ = 'neural_networks'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
