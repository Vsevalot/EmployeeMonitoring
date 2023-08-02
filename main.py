import typing
from typing import Annotated
import functools
import datetime

from fastapi import FastAPI, Response, Header
import fire
from pydantic import BaseModel

from ext import alembic_tools
from ports import rdbs
from config import DBConfig


IdentifierType: typing.TypeAlias = int


app = FastAPI(title="Employee well-being monitoring API")


class RegisterBody(BaseModel):
    first_name: str
    last_name: str
    surname: str
    birthdate: datetime.date
    company: str
    position: str
    phone: str
    email: str
    password: str


@app.post("/v1/register")
async def register_user(
        body: RegisterBody,
) -> Response:
    return Response(status_code=201)


class LoginBody(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    res: str


@app.get("/v1/login")
async def login_user(
        body: LoginBody,
) -> LoginResponse:
    return LoginResponse(res="test")


class InstructionResponse(BaseModel):
    res: str


@app.get("/v1/instructions")
async def get_instruction(
        authorization: Annotated[str | None, Header()],
) -> InstructionResponse:
    return InstructionResponse(res="test")


class State(BaseModel):
    id: IdentifierType
    value: str


class StatesResponse(BaseModel):
    res: list[State]


@app.get("/v1/states")
async def get_states(
        authorization: Annotated[str | None, Header()],
) -> StatesResponse:
    return StatesResponse(res=[State(id=i, value=f'value {i}') for i in range(1, 4)])


class Factor(BaseModel):
    id: IdentifierType
    value: str


class FactorCategory(BaseModel):
    id: IdentifierType
    name: str
    factors: list[Factor]


class FactorsResponse(BaseModel):
    res: list[FactorCategory]


@app.get("/v1/factors")
async def get_factors(
        authorization: Annotated[str | None, Header()],
) -> FactorsResponse:
    return FactorsResponse(res=[])


class FeedbackResponse(BaseModel):
    morning: bool
    evening: bool


@app.get("/v1/feedbacks/{feedback_date}")
async def get_instruction(
        authorization: Annotated[str | None, Header()],
        feedback_date: datetime.date,
) -> FeedbackResponse:
    return FeedbackResponse(morning=False, evening=False)


class MorningBody(BaseModel):
    state_id: IdentifierType


@app.post("/v1/feedbacks/{feedback_date}/morning")
async def save_morning(
        authorization: Annotated[str | None, Header()],
        feedback_date: datetime.date,
        body: MorningBody,
) -> Response:
    return Response(status_code=201)


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None


@app.post("/v1/feedbacks/{feedback_date}/evening")
async def save_evening(
        authorization: Annotated[str | None, Header()],
        feedback_date: datetime.date,
        body: EveningBody,
) -> Response:
    return Response(status_code=201)


class ParticipantListItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    birthdate: datetime.date
    company: str
    position: str
    phone: str
    email: str


class ParticipantResponse(BaseModel):
    res: list[ParticipantListItem]


@app.get("/v1/participants")
async def get_participants(
        authorization: Annotated[str | None, Header()],
) -> ParticipantResponse:
    return ParticipantResponse(res=[])


def launch():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)


from time import sleep


if __name__ == "__main__":
    db_config = DBConfig()

    migrations_rdbs_args = dict(
        db_dsn=db_config.dsn,
        metadata=rdbs.generic.db_metadata,
        migrations_source=rdbs.migrations,
    )
    fire.Fire(
        {
            "api:run": launch,
            "rdbs:upgrade": functools.partial(
                alembic_tools.commands.upgrade, **migrations_rdbs_args
            ),
            "rdbs:downgrade": functools.partial(
                alembic_tools.commands.downgrade, **migrations_rdbs_args
            ),
            "rdbs:create_auto_migration": lambda message: functools.partial(
                alembic_tools.commands.create_auto_migration,
                message=message,
                offline=False,
                **migrations_rdbs_args
            ),
            "rdbs:create_empty_migration": lambda message: functools.partial(
                alembic_tools.commands.create_empty_migration,
                message=message,
                **migrations_rdbs_args
            ),
        }
    )
