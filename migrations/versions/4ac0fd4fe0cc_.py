"""empty message

Revision ID: 4ac0fd4fe0cc
Revises: cc316406c7dd
Create Date: 2020-04-12 21:50:43.289945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import json

# revision identifiers, used by Alembic.
revision = '4ac0fd4fe0cc'
down_revision = 'cc316406c7dd'
branch_labels = None
depends_on = None
building_id = 0


def serialize_building(building_data, neighborhood_id_by_name):
    global building_id
    building_id += 1

    return {
        'id': building_id,
        'neighborhood_id': neighborhood_id_by_name[building_data['neighborhoodName']],
        'attributes': building_data['attributes'],
        'geometry': building_data['geometry']
    }


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    buildings_table = op.create_table('buildings',
                                      sa.Column('id', sa.Integer(), nullable=False),
                                      sa.Column('neighborhood_id', sa.Integer(), nullable=True),
                                      sa.Column('attributes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
                                      sa.Column('geometry', postgresql.JSON(astext_type=sa.Text()), nullable=True),
                                      sa.ForeignKeyConstraint(['neighborhood_id'], ['neighborhoods.id'], ),
                                      sa.PrimaryKeyConstraint('id')
                                      )
    # ### end Alembic commands ###

    # Get all buildings
    conn = op.get_bind()
    res = conn.execute("select id, name from neighborhoods")
    results = res.fetchall()
    all_neighborhoods = [{'id': r[0], 'name': r[1]} for r in results]

    # Get neighborhood ID by the name
    neighborhood_id_by_name = {}

    for neighborhood in all_neighborhoods:
        neighborhood_id_by_name[neighborhood['name']] = neighborhood['id']

    # Load buildings
    with open('./seed_data/buildings.json', encoding='utf-8') as json_file:
        building_data = json.load(json_file)

    # Inserting data to DB
    op.bulk_insert(buildings_table, list(
        map(lambda b: serialize_building(b, neighborhood_id_by_name), building_data)))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('buildings')
    # ### end Alembic commands ###
