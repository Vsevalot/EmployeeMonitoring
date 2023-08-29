from domain.entities import State
from utils import UnitOfWorkRDBS


class StateService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_list(self) -> list[State]:
        async with self._uow:
            return await self._uow.state.get_list()
