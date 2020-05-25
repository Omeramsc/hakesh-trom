from models import Neighborhood, Team, User, buildings_teams_association_table, Campaign
from db import db
from .consts import DEFAULT_TEAM_USER_PASSWORD
from sqlalchemy import func, distinct
import xlsxwriter
from io import BytesIO


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


def generate_users_data(users):
    """
    Generate users' rows (assuming the user's password is the defualt one)
    :param users:
    :return:
    """
    headers = ['שם משתמש', 'סיסמה']
    rows = [[user.username, DEFAULT_TEAM_USER_PASSWORD] for user in users]
    rows.insert(0, headers)

    return rows


def generate_teams_data(teams):
    """
    Generate teams' rows for the reports with the buildings' data
    :param teams:
    :return:
    """
    rows = [['צוות', 'כתובות', 'קומות', 'צפי רווח']]

    for team in teams:
        team_name = team.name or "צוות {}".format(team.id)

        for building in team.buildings:
            serialized_building = building.serialize()
            row = [team_name, serialized_building['address'], serialized_building['number_of_floors'],
                   serialized_building['predicted_earnings']]
            rows.append(row)

    return rows


def write_rows_in_worksheet(worksheet, rows):
    """
    Write rows into a given worksheet
    :param worksheet:
    :param rows:
    :return:
    """
    # Start from the first cell. Rows and columns are zero indexed.
    row_index = 0
    col_index = 0

    # Iterate over the data and write it out row by row.
    for row in rows:
        for item in row:
            worksheet.write(row_index, col_index, item)
            col_index += 1

        row_index += 1
        col_index = 0

    return worksheet


def export_neighborhood_to_excel(campaign_id, neighborhood_id, users):
    """
    Export neighborhood data to excel:
    * Users with passwords
    * Teams' routes
    :param campaign_id:
    :param neighborhood_id:
    :param users:
    :return: BytesIO of excel report
    """

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    users_worksheet = workbook.add_worksheet('משתמשים')
    users_worksheet.right_to_left()
    write_rows_in_worksheet(users_worksheet, generate_users_data(users))

    routes_worksheet = workbook.add_worksheet('מסלולים')
    routes_worksheet.right_to_left()
    teams = db.session.query(Team).join(Campaign).join(Neighborhood).filter(
        Campaign.id == campaign_id).filter(Neighborhood.id == neighborhood_id)
    write_rows_in_worksheet(routes_worksheet, generate_teams_data(teams))

    workbook.close()
    output.seek(0)

    return output
