"""initfactors

Revision ID: 6306cb603de7
Revises: 2f4c86385efd
Create Date: 2023-08-24 22:27:29.532340

"""
from alembic import op
import sqlalchemy as sa
from ports.rdbs.generic import category, factor, user, permission, state
from contracts import Permissions
# from ports.api.v1.schemas import States


# revision identifiers, used by Alembic.
revision = "6306cb603de7"
down_revision = "8f4d065be343"
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
    category_names = (
        "Начальство",
        "Коллеги",
        "Условия работы",
        "Личные факторы и здоровье",
    )
    categories = [dict(id=i, name=name) for i, name in enumerate(category_names)]

    manager_factor_names = """демонстрирует негативные (деструктивные) черты характера
    проявляет профессиональную некомпетентность
    не желает конструктивно взаимодействовать
    оказывает психологическое давление
    показывает неуважение
    отказывается решать проблемы
    принуждает к сверхнормативной работе
    другое""".split("\n")
    manager_factor_names = [n.strip() for n in manager_factor_names]
    manager_factors = [
        dict(category_id=0, name=name, type="text" if name == "другое" else "single")
        for name in manager_factor_names
    ]

    colleague_factor_names = """демонстрируют негативные (деструктивные) черты характера
    проявляют профессиональную некомпетентность
    не желают конструктивно взаимодействовать
    оказывают психологическое давление
    показывают неуважение
    отказываются сотрудничать
    другое""".split("\n")
    colleague_factor_names = [n.strip() for n in colleague_factor_names]
    colleague_factors = [
        dict(category_id=1, name=name, type="text" if name == "другое" else "single")
        for name in colleague_factor_names
    ]

    work_factor_names = """некомфортные условия (температура, запыленность, шум и т.п.)
    слишком высокая интенсивность работы
    высокий уровень стресса
    необходимость работать сверхурочно
    простой из-за поломки оборудования или оргтехники
    плохая организация рабочего процесса
    другое""".split("\n")
    work_factor_names = [n.strip() for n in work_factor_names]
    work_factors = [
        dict(category_id=2, name=name, type="text" if name == "другое" else "single")
        for name in work_factor_names
    ]

    personal_factor_names = """проблемы в личной жизни
    низкий уровень мотивации к работе
    усталость и упадок сил
    плохое физическое самочувствие (нездоровится)
    плохое эмоциональное самочувствие (переживания, нет настроения и т.п.)
    необходимость работать, несмотря на болезнь
    другое""".split("\n")
    personal_factor_names = [n.strip() for n in personal_factor_names]
    personal_factors = [
        dict(category_id=3, name=name, type="text" if name == "другое" else "single")
        for name in personal_factor_names
    ]

    op.execute(sa.insert(category).values(categories))
    op.execute(
        sa.insert(factor).values(
            manager_factors + colleague_factors + work_factors + personal_factors
        )
    )


def add_states(): ...
    # states = [m.value for m in States]
    # op.execute(sa.insert(state).values(states))


def upgrade():
    add_admin()
    add_categories()
    add_states()


def downgrade():
    raise NotImplemented
