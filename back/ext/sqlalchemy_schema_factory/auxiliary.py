import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime, String


class utcnow(expression.FunctionElement):
    type = DateTime()


class uuid(expression.FunctionElement):
    type = String()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def compile_query(
    query: typing.Union[
        sqlalchemy.sql.Select,
        sqlalchemy.sql.Update,
        sqlalchemy.sql.Insert,
        sqlalchemy.sql.Delete,
    ],
) -> str:
    return query.compile(
        compile_kwargs=dict(
            literal_binds=True,
        ),
        dialect=sqlalchemy.dialects.postgresql.dialect(),
    ).string
