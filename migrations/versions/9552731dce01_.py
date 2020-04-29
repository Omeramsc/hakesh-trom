"""empty message

Revision ID: 9552731dce01
Revises: f6b75c436869
Create Date: 2020-04-27 20:21:56.381960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9552731dce01'
down_revision = 'f6b75c436869'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creation_time', sa.DateTime(), nullable=False),
    sa.Column('is_open', sa.Boolean(), nullable=False),
    sa.Column('response', sa.String(), nullable=True),
    sa.Column('response_time', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports')
    # ### end Alembic commands ###
