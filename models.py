from db import db
from datetime import datetime


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    goal = db.Column(db.Float())
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)
    # NEED DATETIME TIMEZONE TO BE IST

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
