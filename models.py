from db import db
from time import localtime, strftime
from app_init import login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    users = db.relationship("User", back_populates="team")
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    campaign = db.relationship("Campaign", back_populates="teams")
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'))
    neighborhood = db.relationship("Neighborhood", back_populates="teams")

    def __init__(self, neighborhood_id, campaign_id):
        self.neighborhood_id = neighborhood_id
        self.campaign_id = campaign_id


class Neighborhood(db.Model):
    __tablename__ = 'neighborhoods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city_name = db.Column(db.String, nullable=False)
    geometry = db.Column(JSON)
    teams = db.relationship("Team", back_populates="neighborhood")

    def __init__(self, name, city_name, geometry):
        self.name = name
        self.city_name = city_name
        self.geometry = geometry

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    goal = db.Column(db.Float())
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=strftime("%d-%m-%Y %H:%M:%S", localtime()))
    teams = db.relationship("Team", back_populates="campaign")

    def __init__(self, name, city, start_date, goal):
        self.name = name
        self.city = city
        self.start_date = start_date
        self.goal = goal

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
    creation_date = db.Column(db.DateTime, nullable=False, default=strftime("%d-%m-%Y %H:%M:%S", localtime()))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship("Team", back_populates="users")

    def __init__(self, username, password, is_admin=False, is_active=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

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
