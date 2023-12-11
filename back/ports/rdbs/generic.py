from ext.sqlalchemy_schema_factory import factory
import sqlalchemy
from sqlalchemy.dialects.postgresql import BYTEA


db_metadata = factory.metadata()

company = factory.table(
    name="companies",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="name", length=150, nullable=False),
    ),
)

organisation_unit = factory.table(
    name="organisation_units",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="name", length=150, nullable=False),
        factory.foreign_key(
            name="company_id",
            to_=company,
            type_=sqlalchemy.INTEGER,
            nullable=False,
        ),
    ),
)

user = factory.table(
    name="users",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="email", length=100, nullable=False, unique=True),
        sqlalchemy.Column("password", BYTEA(length=32)),
        sqlalchemy.Column("salt", BYTEA(length=16)),
        factory.string(name="first_name", length=100, nullable=True),
        factory.string(name="last_name", length=150, nullable=True),
        factory.string(name="surname", length=150, nullable=True),
        factory.date(name="birthdate", nullable=True),
        factory.foreign_key(
            name="organisation_unit_id",
            to_=organisation_unit,
            type_=sqlalchemy.INTEGER,
            nullable=True,
        ),
        factory.string(name="position", length=150, nullable=True),
        factory.string(name="phone", length=100, nullable=True),
        factory.string(name="role", length=20, nullable=True),
        factory.string(name="code", length=20, nullable=True, unique=True),
    ),
)

permission = factory.table(
    name="permissions",
    db_metadata=db_metadata,
    columns=(
        factory.foreign_key(to_=user, type_=sqlalchemy.INTEGER, name="user_id"),
        factory.string(name="permission", length=100),
    ),
    constraints=[sqlalchemy.UniqueConstraint("user_id", "permission")],
)


session = factory.table(
    name="sessions",
    db_metadata=db_metadata,
    columns=(
        factory.foreign_key(to_=user, type_=sqlalchemy.INTEGER, name="user_id"),
        factory.string(name="session_id", length=36),
    ),
    constraints=[sqlalchemy.UniqueConstraint("user_id")],
)

category = factory.table(
    name="categories",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="name", length=50, nullable=False),
    ),
)

factor = factory.table(
    name="factors",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.foreign_key(to_=category, type_=sqlalchemy.INTEGER, name="category_id"),
        factory.string(name="name", length=100, nullable=False),
        factory.string(name="manager_recommendation", length=1000, nullable=False),
        factory.string(name="personal_recommendation", length=1000, nullable=False),
    ),
)

state = factory.table(
    name="states",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.integer(name="value"),
        factory.string(name="name", length=200, nullable=False),
    ),
)

feedback = factory.table(
    name="feedbacks",
    db_metadata=db_metadata,
    columns=(
        factory.foreign_key(to_=user, type_=sqlalchemy.INTEGER, name="user_id"),
        factory.date(name="date"),
        factory.string(name="day_time", length=20),
        factory.foreign_key(
            to_=state, type_=sqlalchemy.INTEGER, name="state_id", nullable=False,
        ),
        factory.foreign_key(
            to_=factor, type_=sqlalchemy.INTEGER, name="factor_id", nullable=True,
        ),
    ),
    constraints=[sqlalchemy.UniqueConstraint("user_id", "date", "day_time")],
)


device = factory.table(
    name="devices",
    db_metadata=db_metadata,
    columns=(
        factory.string_primary_key(length=50),
        factory.string(name="token", length=200),
    ),
)
