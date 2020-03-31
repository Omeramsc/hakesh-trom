"""empty message

Revision ID: aaaef87dc519
Revises: ee34d06f0286
Create Date: 2020-03-30 21:18:48.286132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaaef87dc519'
down_revision = 'ee34d06f0286'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaigns', sa.Column('city', sa.String(length=50), nullable=False))
    op.add_column('campaigns', sa.Column('creation_date', sa.DateTime(), nullable=False))
    op.alter_column('campaigns', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('campaigns', 'start_date',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('campaigns', 'start_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('campaigns', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('campaigns', 'creation_date')
    op.drop_column('campaigns', 'city')
    # ### end Alembic commands ###
