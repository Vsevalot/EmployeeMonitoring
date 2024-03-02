"""change 24 manager recommendation

Revision ID: 4575385663b0
Revises: 6306cb603de7
Create Date: 2024-03-02 11:11:21.725328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4575385663b0'
down_revision = '6306cb603de7'
branch_labels = None
depends_on = None


def upgrade():
    recommendation = "Поставьте акцент на эмоциональное благополучие. Обратите внимание на психологическое состояние сотрудников. Разработайте программы поддержки и направьте их на ресурсы, где сотрудники могут получить помощь, если они испытывают психологическое давление."
    op.execute(sa.text(f"UPDATE factors SET manager_recommendation='{recommendation}' WHERE id=24"))


def downgrade():
    pass
