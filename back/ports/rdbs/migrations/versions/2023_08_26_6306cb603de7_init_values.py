"""initfactors

Revision ID: 6306cb603de7
Revises: 2f4c86385efd
Create Date: 2023-08-24 22:27:29.532340

"""
from alembic import op
import sqlalchemy as sa
from ports.rdbs.generic import category, factor, user, permission, state
from domain.initial_values import get_categories_and_factors, get_states
from contracts import Permissions


# revision identifiers, used by Alembic.
revision = "6306cb603de7"
down_revision = "f8d1317a21ba"
branch_labels = None
depends_on = None


ADMIN_ID = 0


def add_admin():
    admin = {
        "id": ADMIN_ID,
        "email": "admin",
        # just 'admin' with salt
        "password": b"\xa8\xdbt\x87j\xa9Z\xa1\x97X\x92\xd8\xbc\xe3\x98Tg .\xc1\xf8rk(\xedaV\n\xe6\xb4\xaa\xe7",
        "salt": b"\x85\xb8n\x892RF\xd9h\xad\xad\xe3\xd0w\xa7\xda",
    }
    op.execute(sa.insert(user).values(**admin))
    admin_perms = [{"user_id": ADMIN_ID, "permission": p.value} for p in Permissions]
    op.execute(sa.insert(permission).values(admin_perms))


def add_categories():
    categories, factors = get_categories_and_factors()
    op.execute(sa.insert(category).values(categories))
    op.execute(sa.insert(factor).values(factors))


def add_states():
    states = get_states()
    op.execute(sa.insert(state).values(states))


def upgrade():
    add_admin()
    add_categories()
    add_states()


def downgrade():
    raise NotImplemented
