from domain.entities import Category, Factor
from utils import UnitOfWorkRDBS


class CategoryService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_categories(self) -> list[Category]:
        async with self._uow:
            return await self._uow.category.get_list()
