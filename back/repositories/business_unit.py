from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select

from domain.entities import BusinessUnit, Company
from domain.contracts import IdentifierType
from ports.rdbs.generic import organisation_unit, company
from .common import NotFoundError


class BusinessUnitRepository(ABC):
    @abstractmethod
    async def add_one(self, name: str, company_id: IdentifierType) -> IdentifierType:
        ...

    @abstractmethod
    async def update(self, to_update: BusinessUnit) -> None:
        ...

    @abstractmethod
    async def get(self, id: IdentifierType) -> BusinessUnit:
        ...


class BusinessUnitRepositoryRDBS(BusinessUnitRepository):
    def __init__(
        self,
        connection: AsyncConnection,
    ):
        self._connection = connection

    async def add_one(self, name: str, company_id: IdentifierType) -> IdentifierType:
        stmt = (
            organisation_unit.insert()
            .values(name=name, company_id=company_id)
            .returning(organisation_unit.c.id)
        )
        res = await self._connection.execute(stmt)
        return res.scalar_one()

    async def update(self, to_update: BusinessUnit) -> None:
        stmt = (
            organisation_unit.update()
            .values(
                name=to_update["name"],
                company_id=to_update["company"]["id"],
            )
            .where(organisation_unit.c.id == to_update["id"])
        )
        await self._connection.execute(stmt)

    async def get(self, id: IdentifierType) -> BusinessUnit:
        stmt = (
            select(
                organisation_unit.c.id,
                organisation_unit.c.name,
                company.c.id,
                company.c.name,
            )
            .select_from(
                organisation_unit.join(
                    company,
                    organisation_unit.c.company_id == company.c.id,
                )
            )
            .where(organisation_unit.c.id == id)
        )
        res = await self._connection.execute(stmt)
        res = res.fetchone()
        if not res:
            raise NotFoundError()
        return BusinessUnit(
            id=res[0], name=res[1], company=Company(id=res[2], name=res[3])
        )
