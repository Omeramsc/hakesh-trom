"""empty message

Revision ID: cc316406c7dd
Revises: 9a13b9204047
Create Date: 2020-04-10 19:42:42.305343

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cc316406c7dd'
down_revision = '9a13b9204047'
branch_labels = None
depends_on = None


def upgrade():
    # Adding +1 to the IDs to fix the first admin user created the sequence wasn't updated with it and when trying to
    # create new user, the ID the DB tries to set is `1` but it's already taken
    op.get_bind().execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users)+1);")


def downgrade():
    pass
