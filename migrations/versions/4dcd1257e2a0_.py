"""empty message

Revision ID: 4dcd1257e2a0
Revises: 9f5e026c9e0f
Create Date: 2020-05-09 17:25:39.504446

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '4dcd1257e2a0'
down_revision = '9f5e026c9e0f'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    # 1 -> שדה דוב

    # Select the teams that we need to delete
    res = conn.execute("""
SELECT teams.id AS teams_id 
FROM teams JOIN neighborhoods ON neighborhoods.id = teams.neighborhood_id 
WHERE neighborhoods.id = 1;
    """)
    results = res.fetchall()
    team_ids_to_delete = [str(r[0]) for r in results]

    if team_ids_to_delete:
        # Delete the teams' building
        conn.execute(f"""
DELETE 
FROM buildings_teams
WHERE buildings_teams.team_id in ({",".join(team_ids_to_delete)});
        """)

    # Delete the teams' donations
    conn.execute("""
DELETE FROM donations WHERE donations.id in (
    SELECT donations.id AS donations_id 
    FROM donations JOIN teams ON teams.id = donations.team_id JOIN neighborhoods ON neighborhoods.id = teams.neighborhood_id 
    WHERE neighborhoods.id = 1
);
    """)

    # Delete the teams' users
    conn.execute("""
DELETE FROM users WHERE users.id IN (
    SELECT users.id AS users_id 
    FROM users JOIN teams ON teams.id = users.team_id JOIN neighborhoods ON neighborhoods.id = teams.neighborhood_id 
    WHERE neighborhoods.id = 1
);
    """)

    # Delete the teams
    conn.execute("""
DELETE FROM teams WHERE teams.id IN (
    SELECT teams.id AS teams_id 
    FROM teams JOIN neighborhoods ON neighborhoods.id = teams.neighborhood_id 
    WHERE neighborhoods.id = 1
);
    """)

    # Delete the neighborhood's buildings
    conn.execute("""
DELETE FROM buildings WHERE buildings.id IN (
    SELECT buildings.id AS buildings_id 
    FROM buildings JOIN neighborhoods ON neighborhoods.id = buildings.neighborhood_id 
    WHERE neighborhoods.id = 1
);
    """)

    # Delete the neighborhood
    conn.execute("DELETE FROM neighborhoods WHERE neighborhoods.id = 1;")


def downgrade():
    pass
