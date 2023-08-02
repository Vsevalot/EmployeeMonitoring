from ext.sqlalchemy_schema_factory import factory
import sqlalchemy
from sqlalchemy.dialects.postgresql import BYTEA


db_metadata = factory.metadata()

user = factory.table(
    name="users",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="login", length=50),
        sqlalchemy.Column("hashed_pwd", BYTEA(length=32)),
        sqlalchemy.Column("salt", BYTEA(length=16)),
    ),
)

organisation_unit = factory.actions_tracked_table(
    name="organisation_units",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.string(name="name", length=150, nullable=False),
    ),
)


participant = factory.table(
    name="participants",
    db_metadata=db_metadata,
    columns=(
        factory.integer_primary_key(),
        factory.foreign_key(
            name="user_id",
            to_=user,
            type_=sqlalchemy.INTEGER,
            unique=True,
        ),
        factory.string(name="first_name", length=100, nullable=False),
        factory.string(name="last_name", length=150, nullable=False),
        factory.string(name="surname", length=150, nullable=True),
        factory.date(name="birthdate", nullable=True),
        factory.foreign_key(
            name="organisation_unit_id",
            to_=organisation_unit,
            type_=sqlalchemy.INTEGER,
        ),
        factory.string(name="position", length=150, nullable=True),
        factory.string(name="email", length=100, nullable=True),
        factory.string(name="phone", length=100, nullable=True),
    ),
)


permission = factory.table(
    name="permissions",
    db_metadata=db_metadata,
    columns=(
        factory.foreign_key(to_=user, type_=sqlalchemy.INTEGER, name="user_id"),
        factory.string(name="permission"),
    ),
    constraints=[sqlalchemy.UniqueConstraint("user_id", "permission")],
)
