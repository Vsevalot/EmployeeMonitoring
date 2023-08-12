from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import Table, select

from domain.entities import Company
from domain.contracts import IdentifierType
from .common import StorageRDBS


class CompanyStorage(Protocol):
    async def save(self, company: Company) -> None:
        ...

    async def get(self, id: IdentifierType) -> Company:
        ...


class CompanyStorageRDBSRDBS(StorageRDBS):
    def __init__(self, connection: AsyncConnection, company: Table):
        super().__init__(connection)
        self._company = company

    async def save(self, name: str) -> IdentifierType:
        stmt = self._company.insert().values(name=name).returning(self._company)
        res = await self._connection.execute(stmt)
        res = await res.fetchone()
        return res[0]
