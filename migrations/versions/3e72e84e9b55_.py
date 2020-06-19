"""empty message

Revision ID: 3e72e84e9b55
Revises: a92b018b8c85
Create Date: 2020-06-19 12:52:18.654965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from db import db
from models import Campaign
from utils.teams import delete_team_dependencies

revision = '3e72e84e9b55'
down_revision = 'a92b018b8c85'
branch_labels = None
depends_on = None


def upgrade():
    campaigns = Campaign.query.all()
    for campaign in campaigns:
        for team in campaign.teams:
            delete_team_dependencies(team)
            db.session.delete(team)

        db.session.delete(campaign)
    db.session.commit()

    # Resetting team IDs
    op.get_bind().execute("SELECT setval('teams_id_seq', 1);")


def downgrade():
    pass
