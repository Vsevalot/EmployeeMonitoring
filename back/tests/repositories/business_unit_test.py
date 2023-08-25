import pytest

from domain.entities import BusinessUnit, Company
from repositories.business_unit import BusinessUnitRepositoryInMemory, BusinessUnitRepository
from repositories.common import NotFoundError


async def creation(storage: BusinessUnitRepository):
    test_company = Company(id=1, name='Test company')
    test_name = 'Test'
    created = await storage.create(name=test_name, company=test_company)
    assert created == BusinessUnit(id=1, name=test_name, company=test_company)
    await storage.save(created)

    second_test_name = 'Test2'
    second = await storage.create(name=second_test_name, company=test_company)
    assert second == BusinessUnit(id=2, name=second_test_name, company=test_company)


async def save(storage: BusinessUnitRepository):
    test_company = Company(id=1, name='Test')
    test_entity = BusinessUnit(id=1, name='Test', company=test_company)
    await storage.save(test_entity)

    storage_entity = await storage.get(test_entity['id'])
    assert storage_entity == test_entity

    test_entity['name'] = 'new name'
    assert storage_entity != test_entity


async def not_found(storage: BusinessUnitRepository):
    with pytest.raises(NotFoundError):
        await storage.get(1)


@pytest.mark.asyncio
async def test_in_memory():
    storage = BusinessUnitRepositoryInMemory()
    await not_found(storage)
    await creation(storage)
    await save(storage)
