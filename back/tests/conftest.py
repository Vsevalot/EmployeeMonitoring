import asyncio
from typing import AsyncGenerator, TypedDict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool


from ports.rdbs.generic import db_metadata, state, category, factor
from domain.initial_values import get_categories_and_factors, get_states
from config import DBConfig
from ports.api.v1.bootstrap import get_application


db_config = DBConfig()
db_config.database = f'test_{db_config.database}'


app = get_application(db_config)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    test_engine = create_async_engine(db_config.dsn, poolclass=NullPool)
    db_metadata.bind = test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(db_metadata.create_all)
        states = get_states()
        await conn.execute(state.insert().values(states))
        categories, factors = get_categories_and_factors()
        await conn.execute(category.insert().values(categories))
        await conn.execute(factor.insert().values(factors))
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(db_metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class Manager(TypedDict):
    first_name: str
    last_name: str
    surname: str
    birthdate: str
    phone: str
    position: str
    email: str
    password: str
    company: str
    department: str


@pytest.fixture(scope="session")
def manager() -> Manager:
    return Manager(
        **{
            "first_name": "Manager firstName",
            "last_name": "Manager lastName",
            "surname": "surname",
            "birthdate": "2023-08-24",
            "phone": "phone",
            "position": "positon",
            "email": "manager@email",
            "password": "password",
            "company": "company1",
            "department": "department1",
        }
    )


class Participant(TypedDict):
    first_name: str
    last_name: str
    surname: str
    birthdate: str
    phone: str
    position: str
    email: str
    password: str
    manager_id: int


@pytest.fixture(scope="session")
def participant() -> Participant:
    return Participant(
        **{
            "first_name": "participant firstName",
            "last_name": "participant lastName",
            "surname": "surname",
            "birthdate": "2023-08-24",
            "phone": "phone",
            "position": "positon",
            "email": "participant@email",
            "password": "password",
            "manager_id": 1,
        }
    )


@pytest.fixture
async def manager_token(client: AsyncClient, manager: Manager) -> str:
    response = await client.post(
        "/api/v1/login",
        json={
            "email": manager["email"],
            "password": manager["password"],
        },
    )
    return response.json()['result']


@pytest.fixture
async def participant_token(client: AsyncClient, participant: Participant) -> str:
    response = await client.post(
        "/api/v1/login",
        json={
            "email": participant["email"],
            "password": participant["password"],
        },
    )
    return response.json()['result']
