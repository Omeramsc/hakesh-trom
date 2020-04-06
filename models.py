from db import db
from time import localtime, strftime
from app_init import login_manager
from flask_login import UserMixin


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    goal = db.Column(db.Float())
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=strftime("%d-%m-%Y %H:%M:%S", localtime()))

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


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=strftime("%d-%m-%Y %H:%M:%S", localtime()))

    def __init__(self, username, password, is_admin=False, is_active=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

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
