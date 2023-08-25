from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, func

from domain.entities import Company
from ports.rdbs.generic import company
from domain.contracts import IdentifierType
from .common import NotFoundError


class CompanyRepository(ABC):
    @abstractmethod
    async def add_one(self, name: str) -> IdentifierType:
        ...

    @abstractmethod
    async def update(self, to_update: Company) -> None:
        ...

    @abstractmethod
    async def get(self, id: IdentifierType) -> Company:
        ...


class CompanyRepositoryRDBS(CompanyRepository):
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def add_one(self, name: str) -> IdentifierType:
        stmt = company.insert().values(name=name).returning(company.c.id)
        res = await self._connection.execute(stmt)
        return res.scalar_one()

    async def update(self, to_update: Company) -> None:
        stmt = (
            company.update()
            .values(name=to_update["name"])
            .where(company.c.id == to_update["id"])
        )
        await self._connection.execute(stmt)

    async def get(self, id: IdentifierType) -> Company:
        stmt = select(company.c.id, company.c.name).where(company.c.id == id)
        res = await self._connection.execute(stmt)
        res = res.fetchone()
        if not res:
            raise NotFoundError
        return Company(id=res[0], name=res[1])
