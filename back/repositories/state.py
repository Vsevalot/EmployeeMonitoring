from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select
from domain.entities import State
from ports.rdbs.generic import state


class StateRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def get_list(self) -> list[State]:
        stmt = select(state.c.id, state.c.name, state.c.value)
        res = await self._connection.execute(stmt)
        res = res.fetchall()
        return [State(id=r.id, name=r.name, value=r.value) for r in res]
