"""empty message

Revision ID: d788d940c324
Revises: aaaef87dc519
Create Date: 2020-04-01 19:42:11.973359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd788d940c324'
down_revision = 'aaaef87dc519'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'campaigns', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'campaigns', type_='unique')
    # ### end Alembic commands ###
