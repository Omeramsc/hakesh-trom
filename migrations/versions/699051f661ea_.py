"""empty message

Revision ID: 699051f661ea
Revises: bea6ab68be68
Create Date: 2020-04-15 19:30:35.620007

"""
from alembic import op
import sqlalchemy as sa
import json
from models import Building, Neighborhood

# revision identifiers, used by Alembic.
revision = '699051f661ea'
down_revision = 'bea6ab68be68'
branch_labels = None
depends_on = None
building_id = 0
neighborhood_id = 0
supported_neighborhood_names = """
'רמת אביב ג
'תכנית ל
(יפו ד' (גבעת התמרים
אזור שדה דב
בבלי
גני צהלה, רמות צהלה
הדר-יוסף
המשתלה
יד אליהו
כוכב הצפון
נוה אביבים וסביבתה
נוה עופר
נופי ים
צהלה
צוקי אביב
צפון יפו
קרית שאול
קרית שלום
רמת-אביב
תל ברוך
""".splitlines()


def is_neighborhood_supported(neighborhood_data):
    return neighborhood_data['attributes']['shem_shchuna'] in supported_neighborhood_names


def serialize_tlv_neighborhood(neighborhood_data):
    global neighborhood_id
    neighborhood_id += 1

    return {
        'id': neighborhood_id,
        'name': neighborhood_data['attributes']['shem_shchuna'],
        'city_name': 'תל - אביב - יפו',
        'geometry': neighborhood_data['geometry']['rings'][0],
        'center_point': neighborhood_data['attributes']['centerPoint'],
    }


def serialize_building(building_data, neighborhood_id_by_name, neighborhood_tlv_id_by_name):
    global building_id
    building_id += 1

    return {
        'id': building_id,
        'neighborhood_id': neighborhood_id_by_name[building_data['neighborhoodName']],
        'attributes': {'gova_simplex_2019': building_data['gova_simplex_2019'], 'ms_komot': building_data['ms_komot'],
                       'max_height': building_data['max_height'], 'min_height': building_data['min_height'],
                       'ms_shchuna': neighborhood_tlv_id_by_name[building_data['neighborhoodName']]},
        'geometry': building_data['geometry'],
        'address': building_data['formattedAddress'],
        'center_point': building_data['centerPoint'],
        'last_campaign_earnings': building_data['currentYearEarnings']
    }


def upgrade():
    conn = op.get_bind()

    # Delete all the old buildings
    conn.execute("DELETE FROM buildings;")
    # Delete all neighborhoods
    conn.execute("DELETE FROM neighborhoods;")

    # Insert the updated neighborhoods
    with open('./seed_data/neighborhoods_with_center.json', encoding='utf-8') as json_file:
        neighborhoods_data = json.load(json_file)
    clean_neighborhoods_data = list(
        map(serialize_tlv_neighborhood,
            filter(is_neighborhood_supported, neighborhoods_data['features'])))

    op.bulk_insert(Neighborhood.__table__, clean_neighborhoods_data)

    # Get TLV's neighborhood id by it's name
    neighborhood_tlv_id_by_name = {}
    for neighborhood_data in neighborhoods_data['features']:
        neighborhood_tlv_id_by_name[neighborhood_data['attributes']['shem_shchuna']] = neighborhood_data['attributes'][
            'ms_shchuna']

    # Get all neighborhoods
    res = conn.execute("select id, name from neighborhoods")
    results = res.fetchall()
    all_neighborhoods = [{'id': r[0], 'name': r[1]} for r in results]

    # Get neighborhood ID by the name
    neighborhood_id_by_name = {}

    for neighborhood in all_neighborhoods:
        neighborhood_id_by_name[neighborhood['name']] = neighborhood['id']

    # Load buildings
    with open('./seed_data/buildings_with_addresses_center.json', encoding='utf-8') as json_file:
        building_data = json.load(json_file)

    # Inserting data to DB
    rows = list(
        map(lambda b: serialize_building(b, neighborhood_id_by_name, neighborhood_tlv_id_by_name), building_data))
    op.bulk_insert(Building.__table__, rows)


def downgrade():
    pass
