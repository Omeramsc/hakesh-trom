from db import db


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    start_date = db.Column(db.Date())
    goal = db.Column(db.Float())

    def __init__(self, name, start_date, goal):
        self.name = name
        self.start_date = start_date
        self.goal = goal

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'goal': self.goal,
            'start_date': self.start_date
        }
