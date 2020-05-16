from db import db
from sqlalchemy import func
from models import Team, Donation


def get_earned_money(team_id):
    return db.session.query(func.sum(Donation.amount)).join(Team).filter(
        Team.id == team_id).scalar()


def delete_team_dependencies(team):
    # Delete the team's building
    team.buildings = []

    for user in team.users:
        db.session.delete(user)
    team.users = []

    for donation in team.donations:
        db.session.delete(donation)
    team.donations = []

    for report in team.reports:
        db.session.delete(report)
    team.reports = []
