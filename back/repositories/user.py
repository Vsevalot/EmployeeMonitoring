from abc import ABC, abstractmethod
import datetime
from collections.abc import Sequence, Mapping
from typing import Any
from operator import eq

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

from domain.entities import User, UserRole, BusinessUnit, Company
from domain.contracts import IdentifierType
from ports.rdbs.generic import user, permission, company, organisation_unit
from .common import NotFoundError, AlreadyInUse


class UserRepository(ABC):
    @abstractmethod
    async def add_one(
        self,
        email: str,
        phone: str,
        password: bytes,
        salt: bytes,
        permissions: Sequence[str],
        first_name: str,
        last_name: str,
        surname: str | None,
        birthdate: datetime.date,
        position: str,
        business_unit_id: IdentifierType,
        role: UserRole,
    ) -> IdentifierType:
        ...

    @abstractmethod
    async def update(self, to_update: User) -> None:
        ...

    @abstractmethod
    async def get(self, id: IdentifierType | None, email: str | None) -> User:
        ...


class UserRepositoryRDBS(UserRepository):
    def __init__(
        self,
        connection: AsyncConnection,
    ):
        self._connection = connection

    async def add_one(
        self,
        email: str,
        phone: str,
        password: bytes,
        salt: bytes,
        permissions: Sequence[str],
        first_name: str,
        last_name: str,
        surname: str | None,
        birthdate: datetime.date,
        position: str,
        organisation_unit_id: IdentifierType,
        role: UserRole,
        code: str | None = None,
    ) -> IdentifierType:
        insert_user_stmt = (
            user.insert()
            .values(
                phone=phone,
                email=email,
                password=password,
                salt=salt,
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                birthdate=birthdate,
                position=position,
                organisation_unit_id=organisation_unit_id,
                role=role.value,
                code=code,
            )
            .returning(user.c.id)
        )
        try:
            res = await self._connection.execute(insert_user_stmt)
        except IntegrityError:
            raise AlreadyInUse("Email already used")
        user_id = res.scalar_one()
        if permissions:
            to_insert = [{"user_id": user_id, "permission": p} for p in permissions]
            insert_perm_stmt = permission.insert().values(to_insert)
            await self._connection.execute(insert_perm_stmt)
        return user_id

    async def update(self, to_update: User) -> None:
        user_stmt = (
            user.update()
            .values(
                phone=to_update["phone"],
                email=to_update["email"],
                hashed_pwd=to_update["password"],
                salt=to_update["salt"],
                first_name=to_update["first_name"],
                last_name=to_update["last_name"],
                surname=to_update["surname"],
                position=to_update["position"],
                busenes_unit_id=to_update["business_unit"]["id"],
                birthdate=to_update["birthdate"],
                role=to_update["role"].value,
            )
            .where(user.c.id == to_update["id"])
        )
        await self._connection.execute(user_stmt)

        delete_old = permission.delete().where(permission.c.user_id == to_update["id"])
        await self._connection.execute(delete_old)
        insert_perm_stmt = permission.insert().values(
            [
                {"user_id": to_update["id"], "permission": p}
                for p in to_update["permissions"]
            ]
        )
        await self._connection.execute(insert_perm_stmt)

    async def get(self, user_id: IdentifierType | None = None, email: str | None = None) -> User:
        if not user_id and not email:
            raise NotFoundError

        stmt = select(
                *self._user_fields,
                func.array_agg(permission.c.permission).label("permissions"),
            ).select_from(self.joined)
        if user_id:
            stmt = stmt.where(user.c.id == user_id)
        if email:
            stmt = stmt.where(user.c.email == email)

        stmt = stmt.group_by(user.c.id, organisation_unit.c.id, company.c.id)
        res = await self._connection.execute(stmt)
        res = res.fetchone()
        if not res:
            raise NotFoundError
        return self._format_user(res)

    @staticmethod
    def _get_filters(filters: Mapping[str, Any]) -> list:
        _filters = {k: v for k, v in filters.items()}
        if "role" in _filters:
            _filters["role"] = _filters["role"].value
        return [
            eq(getattr(user.c, column), value) for column, value in _filters.items()
        ]

    @property
    def joined(self):
        return (
            user.join(
                permission,
                user.c.id == permission.c.user_id,
                isouter=True,
            )
            .join(
                organisation_unit,
                user.c.organisation_unit_id == organisation_unit.c.id,
            )
            .join(
                company,
                organisation_unit.c.company_id == company.c.id,
            )
        )

    async def get_list(self, filters: Mapping[str, Any]) -> list[User]:
        stmt = (
            select(
                *self._user_fields,
                func.array_agg(permission.c.permission).label("permissions"),
            )
            .select_from(self.joined)
            .where(*self._get_filters(filters))
        ).group_by(user.c.id, organisation_unit.c.id, company.c.id)
        res = await self._connection.execute(stmt)
        res = res.fetchall()
        return [self._format_user(r) for r in res]

    @property
    def _user_fields(self):
        return (
            user.c.id,
            user.c.first_name,
            user.c.last_name,
            user.c.surname,
            user.c.birthdate,
            user.c.organisation_unit_id,
            user.c.position,
            user.c.email,
            user.c.phone,
            user.c.role,
            user.c.password,
            user.c.salt,
            organisation_unit.c.name.label("organisation_unit_name"),
            company.c.id.label("company_id"),
            company.c.name.label("company_name"),
            user.c.code,
        )

    @staticmethod
    def _format_user(row) -> User:
        return User(
            id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            surname=row.surname,
            birthdate=row.birthdate,
            email=row.email,
            position=row.position,
            role=UserRole(row.role),
            permissions=row.permissions,
            phone=row.phone,
            business_unit=BusinessUnit(
                id=row.organisation_unit_id,
                name=row.organisation_unit_name,
                company=Company(id=row.company_id, name=row.company_name),
            ),
            password=row.password,
            salt=row.salt,
            code=row.code,
        )
