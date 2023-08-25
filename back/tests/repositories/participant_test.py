import pytest

from services.password import PasswordService
from domain.entities import User, Participant
from repositories.participant import ParticipantRepository, ParticipantRepositoryInMemory
from repositories.common import NotFoundError


async def creation(storage: ParticipantRepository):
    test_email = "Test email"
    test_phone = "Test phone"
    test_permissions = ["Test permission"]
    test_password = "Test password"
    test_hashed_password, test_salt = PasswordService.hash_password(test_password)
    test_user = User(
        id=1,
        email=test_email,
        phone=test_phone,
        password=test_hashed_password,
        salt=test_salt,
        permissions=test_permissions,
    )
    created = await storage.create(
        email=test_email,
        phone=test_phone,
        password=test_hashed_password,
        salt=test_salt,
        permissions=test_permissions,
    )
    await storage.save(created)

    test_email2 = "Test email2"
    test_phone2 = "Test phone2"
    test_permissions2 = ["Test permission2"]
    test_password2 = "Test password2"
    test_hashed_password2, test_salt2 = PasswordService.hash_password(test_password2)
    created2 = await storage.create(
        email=test_email2,
        phone=test_phone2,
        password=test_hashed_password2,
        salt=test_salt2,
        permissions=test_permissions2,
    )
    assert created2 == User(
        id=2,
        email=test_email2,
        phone=test_phone2,
        password=test_hashed_password2,
        salt=test_salt2,
        permissions=test_permissions2,
    )


async def save(storage: ParticipantRepository):
    test_email = "Test email"
    test_phone = "Test phone"
    test_permissions = ["Test permission"]
    test_password = "Test password"
    test_hashed_password, test_salt = PasswordService.hash_password(test_password)
    test_entity = User(
        id=1,
        email=test_email,
        phone=test_phone,
        password=test_hashed_password,
        salt=test_salt,
        permissions=test_permissions,
    )
    await storage.save(test_entity)
    storage_entity = await storage.get(test_entity['id'])
    assert test_entity == storage_entity

    test_entity["phone"] = "new name"
    assert storage_entity != test_entity


async def not_found(storage: ParticipantRepository):
    with pytest.raises(NotFoundError):
        await storage.get(1)


@pytest.mark.asyncio
async def test_in_memory():
    storage = ParticipantRepositoryInMemory()
    await not_found(storage)
    await creation(storage)
    await save(storage)
