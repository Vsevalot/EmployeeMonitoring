from typing import Protocol
import datetime

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import Table, select

from services import PasswordService
from domain.entities import User
from domain.contracts import IdentifierType
from .common import StorageRDBS


class UserStorage(Protocol):
    async def create(
        self,
        first_name: str,
        last_name: str,
        surname: str,
        birthdate: datetime.date,
        phone: str,
        business_unit_id: IdentifierType,
        position: str,
        email: str,
        password: str,
    ) -> None:
        ...

    async def get(self, id: IdentifierType) -> User:
        ...


class UserStorageRDBSRDBS(StorageRDBS):
    def __init__(
        self,
        connection: AsyncConnection,
        user: Table,
        permission: Table,
        password_service: PasswordService,
    ):
        super().__init__(connection)
        self._user = user
        self._permission = permission
        self._password_service = password_service

    async def save(
        self,
        first_name: str,
        last_name: str,
        surname: str,
        birthdate: datetime.date,
        phone: str,
        business_unit_id: IdentifierType,
        position: str,
        email: str,
        password: str,
    ) -> IdentifierType:
        hashed_password, salt = self._password_service.hash_password(password)
        user_stmt = (
            self._user.insert()
            .values(
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                birthdate=birthdate,
                phone=phone,
                email=email,
                business_unit_id=business_unit_id,
                position=position,
                hashed_pwd=hashed_password,
                salt=salt,
            )
            .returning(self._user.c.id)
        )
        res = await self._connection.execute(user_stmt)
        res = await res.fetchone()
        return res[0]

    async def get(self, user_id) -> User:
        joined = self._user.join(
            self._permission, self._user.c.id == self._permission.c.user_id
        )
        stmt = (
            select(self._user, self._permission.c.permission)
            .select_from(joined)
            .where(self._user.c.id == user_id)
        )
        res = await self._connection.execute(stmt)
        res = await res.fetchone()
        print(1)


class UserStorageInMemory:
    def __init__(self):
        self._storage = {}

    async def save(self, user: User) -> None:
        self._storage[user["id"]] = user

    async def get(self, id: IdentifierType) -> User:
        return self._storage[id]
