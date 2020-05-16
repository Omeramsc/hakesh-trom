from models import Neighborhood, Team, User, buildings_teams_association_table, Campaign
from db import db
from .consts import DEFAULT_TEAM_USER_PASSWORD
from sqlalchemy import func, distinct


def serialize_campaign_neighborhoods(neighborhood, campaign_teams):
    """
    Structure the campaign's neighborhood in a nice easy format
    :param neighborhood: neighborhood to serialize
    :param campaign_teams: All the campaign's teams
    :return:
    """

    teams_in_neighborhood = list(filter(lambda t: t.neighborhood_id == neighborhood.id, campaign_teams))
    number_of_routes = db.session.query(
        func.count(distinct(buildings_teams_association_table.columns.team_id))).join(
        Team).filter(Team.id.in_([team.id for team in teams_in_neighborhood])).scalar() or 0

    return {
        'neighborhood_id': neighborhood.id,
        'neighborhood_name': neighborhood.name,
        'number_of_teams': len(teams_in_neighborhood),
        'number_of_routes': number_of_routes
    }


def get_response_campaign_neighborhoods(campaign):
    """
    Get the necessary data to represent the campaign's neighborhoods contort page
    :param campaign:
    :return: available neighborhoods in the campaign's city and the neighborhoods campaign that are already in the campaign
    """

    campaign_teams = campaign.teams
    campaign_neighborhoods = campaign.get_neighborhoods(campaign_teams)
    campaign_neighborhood_ids = list(map(lambda n: n.id, campaign_neighborhoods))

    available_neighborhoods_query = Neighborhood.query \
        .filter(Neighborhood.city_name == campaign.city) \
        .filter(~Neighborhood.id.in_(campaign_neighborhood_ids))

    available_neighborhoods = list(map(lambda n: n.serialize(), available_neighborhoods_query.all()))
    serialized_campaign_neighborhoods = list(map(lambda n: serialize_campaign_neighborhoods(n, campaign_teams),
                                                 campaign_neighborhoods))
    return available_neighborhoods, serialized_campaign_neighborhoods


def create_teams_and_users(campaign_id, neighborhood_id, number_of_teams):
    """
    Create teams for the given camping and neighborhood in bulks
    :param number_of_teams:
    :param campaign_id:
    :param neighborhood_id:
    :return: New users' login info
    """
    return list(map(lambda _: create_team_and_user(campaign_id, neighborhood_id), range(number_of_teams)))


def create_team_and_user(campaign_id, neighborhood_id):
    """
    Create a team of detonators and the corespondent user
    :param campaign_id:
    :param neighborhood_id:
    :return: New user's login info
    """
    # Create new team
    new_team = Team(campaign_id=campaign_id, neighborhood_id=int(neighborhood_id))

    db.session.add(new_team)
    db.session.commit()

    # Create new user
    team_user = User(username="team_{team_id}".format(team_id=new_team.id), password=None, is_admin=False,
                     is_active=True)
    team_user.set_password(DEFAULT_TEAM_USER_PASSWORD)
    team_user.team_id = new_team.id

    db.session.add(team_user)
    db.session.commit()

    return {
        'username': team_user.username,
        'password': DEFAULT_TEAM_USER_PASSWORD
    }


def reset_and_export_users(campaign_id, neighborhood_id):
    users = db.session.query(User).join(Team).join(Campaign).join(Neighborhood).filter(
        Campaign.id == campaign_id).filter(Neighborhood.id == neighborhood_id)

    # Reset passwords
    for user in users:
        user.set_password(DEFAULT_TEAM_USER_PASSWORD)

    db.session.commit()

    headers = ['Username', 'Password']
    rows = [','.join([user.username, DEFAULT_TEAM_USER_PASSWORD]) for user in users]

    return ','.join(headers) + '\n' + '\n'.join(rows) + '\n'
