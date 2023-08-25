import uuid

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select
from domain.contracts import IdentifierType, Token
from ports.rdbs.generic import session


class SessionRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def add_session(self, user_id: IdentifierType) -> Token:
        token = str(uuid.uuid4())
        stmt = session.insert().values(user_id=user_id, session_id=token)
        await self._connection.execute(stmt)
        return token

    async def delete_sessions(self, user_id: IdentifierType) -> None:
        stmt = session.delete().where(session.c.user_id == user_id)
        await self._connection.execute(stmt)

    async def get_user_id(self, token: Token) -> IdentifierType | None:
        stmt = select(session.c.user_id).where(session.c.session_id == token)
        res = await self._connection.execute(stmt)
        return res.scalar()
