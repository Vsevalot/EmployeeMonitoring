import random
import string
from collections.abc import Mapping
from typing import Any

from domain.contracts import IdentifierType, UserRole
from contracts import PARTICIPANT_READ_ORGANISATION
from domain.entities import User
from ports.api.v1.schemas import ManagerRegisterBody, ParticipantRegisterBody
from utils import UnitOfWorkRDBS
from services import PasswordService
from config import MANAGER_CODE_LENGTH


class UserService:
    def __init__(self, uow: UnitOfWorkRDBS, password_service: PasswordService):
        self._uow = uow
        self._password_service = password_service

    @staticmethod
    def _get_random_manager_code(length: int = MANAGER_CODE_LENGTH) -> str:
        return "".join(random.choice(string.ascii_uppercase) for _ in range(length))

    async def add_one_manager(self, data: ManagerRegisterBody) -> IdentifierType:
        hashed_pwd, salt = self._password_service.hash_password(data.password)
        async with self._uow:
            company_id = await self._uow.company.add_one(name=data.company)
            organisation_unit_id = await self._uow.business_unit.add_one(
                name=data.department, company_id=company_id
            )
            user_id = await self._uow.user.add_one(
                phone=data.phone,
                email=data.email,
                position=data.position,
                last_name=data.last_name,
                first_name=data.first_name,
                surname=data.surname,
                password=hashed_pwd,
                salt=salt,
                permissions=[PARTICIPANT_READ_ORGANISATION],
                organisation_unit_id=organisation_unit_id,
                birthdate=data.birthdate,
                role=UserRole.manager,
                code=self._get_random_manager_code(),
            )
            await self._uow.commit()
        return user_id

    async def add_one_participant(
        self, data: ParticipantRegisterBody
    ) -> IdentifierType:
        hashed_pwd, salt = self._password_service.hash_password(data.password)
        async with self._uow:
            manager = await self._uow.user.get(user_id=data.manager_id)
            user_id = await self._uow.user.add_one(
                phone=data.phone,
                email=data.email,
                position=data.position,
                last_name=data.last_name,
                first_name=data.first_name,
                surname=data.surname,
                password=hashed_pwd,
                salt=salt,
                permissions=[],
                organisation_unit_id=manager["business_unit"]["id"],
                birthdate=data.birthdate,
                role=UserRole.participant,
            )
            await self._uow.commit()
        return user_id

    async def get_user(
        self,
        user_id: IdentifierType | None = None,
        email: str | None = None,
    ) -> User:
        async with self._uow:
            return await self._uow.user.get(user_id=user_id, email=email)

    async def get_list(self, filters: Mapping[str, Any] | None = None) -> list[User]:
        async with self._uow:
            return await self._uow.user.get_list(filters or {})
