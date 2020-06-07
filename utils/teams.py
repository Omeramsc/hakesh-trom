from db import db
from sqlalchemy import func
from models import Team, Donation


def get_earned_money(team_id):
    return db.session.query(func.sum(Donation.amount)).join(Team).filter(
        Team.id == team_id).scalar()


def get_team_progress(team):
    progress = {
        'total_earnings': get_earned_money(team.id) or 0,
        'predicted_total': team.serialize()['predicted_total'],
    }
    if progress['predicted_total']:
        progress['percentage'] = progress['total_earnings'] / progress['predicted_total'] * 100
    else:
        progress['percentage'] = 0
    return progress


def delete_team_dependencies(team):
    # Delete the team's building
    team.buildings = []

    for user in team.users:
        for notification in user.notifications:
            db.session.delete(notification)
        user.notifications = []
        db.session.delete(user)
    team.users = []

    for donation in team.donations:
        for invoice in donation.invoice:
            db.session.delete(invoice)
        donation.invoice = []
        db.session.delete(donation)
    team.donations = []

    for report in team.reports:
        for notification in report.notification:
            db.session.delete(notification)
        report.notification = []
        db.session.delete(report)
    team.reports = []
