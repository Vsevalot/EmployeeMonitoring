"""admin

Revision ID: b3ae82577065
Revises: ce6c419ad41b
Create Date: 2023-08-02 18:04:55.757098

"""
import sqlalchemy
from alembic import op
from ports.rdbs.generic import user, permission
from contracts import Permissions


# revision identifiers, used by Alembic.
revision = 'b3ae82577065'
down_revision = 'af34b92adb7d'
branch_labels = None
depends_on = None

ADMIN_ID = 0


def upgrade():
    admin = {
        "id": ADMIN_ID,
        "login": "admin",
        # just 'admin' with salt
        "hashed_pwd": b'\xa8\xdbt\x87j\xa9Z\xa1\x97X\x92\xd8\xbc\xe3\x98Tg .\xc1\xf8rk(\xedaV\n\xe6\xb4\xaa\xe7',
        "salt": b'\x85\xb8n\x892RF\xd9h\xad\xad\xe3\xd0w\xa7\xda',
    }
    op.execute(sqlalchemy.insert(user).values(**admin))
    admin_perms = [{"user_id": ADMIN_ID, "permission": p.value} for p in Permissions]
    op.execute(sqlalchemy.insert(permission).values(admin_perms))


def downgrade():
    op.execute(sqltext=sqlalchemy.text(f"DELETE FROM permissions WHERE user_id={ADMIN_ID}"))
    op.execute(sqltext=sqlalchemy.text(f"DELETE FROM users WHERE id={ADMIN_ID}"))
