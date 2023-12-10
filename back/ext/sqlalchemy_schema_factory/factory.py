import typing
from enum import Enum

import sqlalchemy
import sqlalchemy.sql
import sqlalchemy.dialects.postgresql
from . import conventions, auxiliary as aux


def column(
    name: str,
    *args,
    **kwargs,
) -> sqlalchemy.Column:
    return sqlalchemy.Column(
        name,
        *args,
        **kwargs,
    )


def integer_primary_key() -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        autoincrement=True,
        primary_key=True,
    )


def uuid_primary_key(autogenerate: bool = False) -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "id",
        sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=sqlalchemy.sql.func.uuid_generate_v4() if autogenerate else None
    )


def string_primary_key(length: int = 20) -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "id", sqlalchemy.String(length=length), primary_key=True, nullable=False
    )


def integer_autoincrement(is_indexed: bool = True) -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "id", sqlalchemy.Integer, autoincrement=True, index=is_indexed, nullable=False
    )


def boolean(
    name: str,
    index: bool = True,
    nullable: bool = False,
    default: bool = False,
) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.Boolean,
        index=index,
        nullable=nullable,
        default=default,
    )


def string(
    name: str,
    length: typing.Optional[int] = None,
    index: bool = False,
    nullable: bool = True,
    unique: bool = False,
    server_default: typing.Optional[str] = None,
    **kwargs,
) -> sqlalchemy.Column:
    if length:
        type_ = sqlalchemy.String(length)
    else:
        type_ = sqlalchemy.String
    return column(
        name,
        type_,
        index=index,
        nullable=nullable,
        unique=unique,
        server_default=server_default,
        **kwargs,
    )


def text(name: str, index: bool = False, nullable: bool = True, **kwargs) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.Text,
        index=index,
        nullable=nullable,
        **kwargs,
    )


def jsonb(name: str, index: bool = False, nullable: bool = True, **kwargs) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.dialects.postgresql.JSONB,
        index=index,
        nullable=nullable,
        **kwargs,
    )


def integer(
    name: str,
    index: bool = False,
    nullable: bool = False,
    default: typing.Optional[int] = None,
    server_default: typing.Optional[str] = None,
    **kwargs,
) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.Integer,
        index=index,
        nullable=nullable,
        default=default,
        server_default=server_default,
        **kwargs,
    )


def uuid(
    name: str,
    index: bool = False,
    nullable: bool = False,
    default: typing.Optional[int] = None,
    server_default: typing.Optional[str] = None,
    **kwargs,
) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        index=index,
        nullable=nullable,
        default=default,
        server_default=server_default,
        **kwargs,
    )


def datetime(
    name: str,
    **kwargs,
) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.DateTime,
        **kwargs,
    )


def date(
    name: str,
    nullable: bool = True,
    **kwargs,
) -> sqlalchemy.Column:
    return column(
        name,
        sqlalchemy.Date,
        nullable=nullable,
        **kwargs,
    )


def enum(name: str, type_: typing.Type[Enum], nullable: bool = True, **kwargs) -> sqlalchemy.Column:
    return column(name, sqlalchemy.Enum(type_, name=f"type_{name}"), nullable=nullable, **kwargs)


def array(
    name: str,
    type_: typing.Union[
        typing.Type[sqlalchemy.Integer],
        typing.Type[sqlalchemy.String],
        typing.Type[sqlalchemy.Boolean],
        typing.Type[sqlalchemy.UUID],
    ],
    **kwargs,
) -> sqlalchemy.Column:
    return column(name, sqlalchemy.dialects.postgresql.ARRAY(type_), **kwargs)


def default_datetime(
    name: str,
    **kwargs,
) -> sqlalchemy.Column:
    return datetime(
        name,
        nullable=False,
        server_default=aux.utcnow(),
        **kwargs,
    )


def server_updatable_datetime(name: str, **kwargs) -> sqlalchemy.Column:
    return datetime(
        name,
        nullable=True,
        onupdate=aux.utcnow(),
        **kwargs,
    )


def foreign_key(
    to_: sqlalchemy.Table | typing.Callable | None = None,
    type_: sqlalchemy.dialects.postgresql.UUID
           | sqlalchemy.Integer
           | sqlalchemy.String = sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
    name: str = None,
    on_: sqlalchemy.Column = None,
    index: bool = True,
    unique: bool = False,
    nullable: bool = False,
) -> sqlalchemy.Column:
    if on_ is None:
        on_ = to_.c.id
    name = name or f"{to_.name}_id"
    return column(
        name,
        type_,
        sqlalchemy.ForeignKey(on_),
        index=index,
        unique=unique,
        nullable=nullable,
    )


def unique_constraint(
    columns: typing.Sequence[str],
    name: typing.Optional[str] = None,
) -> sqlalchemy.UniqueConstraint:
    kwargs = dict()
    if name:
        kwargs["name"] = name
    return sqlalchemy.UniqueConstraint(
        *columns,
        **kwargs,
    )


def table(
    name: str,
    db_metadata: sqlalchemy.MetaData,
    columns: typing.Sequence[sqlalchemy.Column],
    constraints: typing.Sequence[sqlalchemy.Constraint] = (),
) -> sqlalchemy.Table:
    return sqlalchemy.Table(
        name,
        db_metadata,
        *columns,
        *constraints,
    )


def actions_tracked_table(
    name: str,
    db_metadata: sqlalchemy.MetaData,
    columns: typing.Sequence[sqlalchemy.Column],
    constraints: typing.Sequence[sqlalchemy.Constraint] = (),
    can_be_deleted: bool = True,
) -> sqlalchemy.Table:
    columns = list(columns)
    columns.extend([default_datetime("created_at"), server_updatable_datetime("updated_at")])
    if can_be_deleted:
        columns.append(datetime("deleted_at", nullable=True))
    return table(name=name, db_metadata=db_metadata, columns=columns, constraints=constraints)


def metadata(
    naming_convention: typing.MutableMapping[str, typing.Any] = conventions.naming_convention
) -> sqlalchemy.MetaData:
    return sqlalchemy.MetaData(naming_convention=naming_convention)
