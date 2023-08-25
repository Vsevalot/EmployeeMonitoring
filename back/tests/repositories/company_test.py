import pytest

from domain.entities import Company
from repositories.company import CompanyRepositoryInMemory, CompanyRepository
from repositories.common import NotFoundError


async def creation(storage: CompanyRepository):
    test_name = 'Test'
    created = await storage.create(name=test_name)
    assert created == Company(id=1, name=test_name)
    await storage.save(created)
    
    second_test_name = 'Test2'
    second = await storage.create(name=second_test_name)
    assert second == Company(id=2, name=second_test_name)


async def save(storage: CompanyRepository):
    test_entity = Company(id=1, name='Test')
    await storage.save(test_entity)
    storage_entity = await storage.get(test_entity['id'])
    assert storage_entity == test_entity

    test_entity['name'] = 'new name'
    assert storage_entity != test_entity


async def not_found(storage: CompanyRepository):
    with pytest.raises(NotFoundError):
        await storage.get(1)


@pytest.mark.asyncio
async def test_in_memory():
    storage = CompanyRepositoryInMemory()
    await not_found(storage)
    await creation(storage)
    await save(storage)
