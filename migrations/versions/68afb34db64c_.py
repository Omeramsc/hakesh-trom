"""empty message

Revision ID: 68afb34db64c
Revises: 4dcd1257e2a0
Create Date: 2020-05-23 14:34:23.210695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68afb34db64c'
down_revision = '4dcd1257e2a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('was_read', sa.Boolean(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###
