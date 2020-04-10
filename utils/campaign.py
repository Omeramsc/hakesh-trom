from models import Neighborhood, Team, User
from db import db
from .consts import DEFAULT_TEAM_USER_PASSWORD
import functools


def serialize_campaign_neighborhoods(neighborhood, campaign_teams):
    """
    Structure the campaign's neighborhood in a nice easy format
    :param neighborhood: neighborhood to serialize
    :param campaign_teams: All the campaign's teams
    :return:
    """
    # Represent each team in `1` or `0` if related to the current neighborhood
    teams_representation = map(lambda t: (1 if t.neighborhood_id == neighborhood.id else 0), campaign_teams)

    return {
        'neighborhood_id': neighborhood.id,
        'neighborhood_name': neighborhood.name,
        'number_of_teams': functools.reduce(lambda x, y: x + y, teams_representation),
        'number_of_routes': 0
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
