from db import db


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
