"""removed drugoe

Revision ID: 260f84a68617
Revises: 559b173d8148
Create Date: 2023-10-28 10:34:26.980624

"""
from alembic import op
import sqlalchemy as sa

from ports.rdbs.generic import category

# revision identifiers, used by Alembic.
revision = '260f84a68617'
down_revision = '559b173d8148'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("DELETE FROM factors WHERE name='другое'"))


def downgrade():
    pass
