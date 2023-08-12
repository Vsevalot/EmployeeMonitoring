from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import Table, select

from domain.entities import BusinessUnit, Company
from domain.contracts import IdentifierType
from .common import StorageRDBS


class BusinessUnitStorage(Protocol):
    async def save(self, business_unit: BusinessUnit) -> None:
        ...

    async def get(self, id: IdentifierType) -> BusinessUnit:
        ...


class BusinessUnitStorageRDBSRDBS(StorageRDBS):
    def __init__(
        self,
        connection: AsyncConnection,
        company: Table,
        business_unit: Table,
    ):
        super().__init__(connection)
        self._business_unit = business_unit
        self._company = company

    async def save(self, name: str, company_id: IdentifierType) -> IdentifierType:
        insert_stmt = (
            self._business_unit.insert()
            .values(name=name, company_id=company_id)
            .returning(self._business_unit.c.id)
        )
        res = await self._connection.execute(insert_stmt)
        res = await res.fetchone()
        return res[0]

    async def get(self, id: IdentifierType) -> BusinessUnit:
        stmt = (
            select(
                self._business_unit.c.id,
                self._business_unit.c.name,
                self._company.c.id,
                self._company.c.name,
            )
            .select_from(
                self._business_unit.join(
                    self._company,
                    self._business_unit.c.company_id == self._company.c.id,
                )
            )
            .where(self._business_unit.c.id == id)
        )
        res = await self._connection.execute(stmt)
        res = await res.fetchone()
        return BusinessUnit(
            id=res[0], name=res[1], company=Company(id=res[2], name=res[3])
        )

