from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel
import datetime
from domain.contracts import IdentifierType, FactorType, DayTime
from domain.entities import User, Feedback


class MorningBody(BaseModel):
    state_id: IdentifierType


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None = None
    value: str | None = None


class State(BaseModel):
    id: IdentifierType
    name: str
    value: int


class FeedbackResponse(BaseModel):
    morning: State | None = None
    evening: State | None = None

    @classmethod
    def from_feedbacks(cls, morning: Feedback | None, evening: Feedback | None):
        if morning:
            morning = State(
                id=morning["state"].id,
                name=morning["state"].name,
                value=morning["state"].value,
            )
        if evening:
            evening = State(
                id=evening["state"].id,
                name=evening["state"].name,
                value=evening["state"].value,
            )
        return cls(
            morning=morning,
            evening=evening,
        )


class Factor(BaseModel):
    id: IdentifierType
    name: str
    type: FactorType


class Category(BaseModel):
    id: IdentifierType
    name: str
    factors: list[Factor]


class FactorsResponse(BaseModel):
    result: list[Category]


class InstructionResponse(BaseModel):
    result: str


class StatesResponse(BaseModel):
    result: list[State]


class RegisterBodyBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    birthdate: datetime.date
    phone: str
    position: str
    email: str
    password: str


class ManagerRegisterBody(RegisterBodyBase):
    company: str
    department: str


class ParticipantRegisterBody(RegisterBodyBase):
    manager_id: IdentifierType


class LoginBody(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    result: str


class Participant(BaseModel):
    id: IdentifierType
    first_name: str | None
    last_name: str | None
    surname: str | None
    birthdate: datetime.date | None
    company: str | None
    position: str | None
    phone: str | None
    email: str

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            surname=user["surname"],
            phone=user["phone"],
            company=user["business_unit"]["company"]["name"],
            position=user["position"],
            email=user["email"],
            birthdate=user["birthdate"],
        )


class ParticipantListResponse(BaseModel):
    result: list[Participant]


class ParticipantSingleResponse(BaseModel):
    result: Participant


class ManagerListItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    department: str
    company: str


class ManagerListResponse(BaseModel):
    result: list[ManagerListItem]


class ManagerResponse(BaseModel):
    result: str


class RecommendationsResponse(BaseModel):
    result: str


class GroupStatItem(BaseModel):
    category: str
    voted: int


class GroupStatResponse(BaseModel):
    result: list[GroupStatItem]

    @classmethod
    def from_feedbacks(cls, feedbacks: Sequence[Feedback]):
        res = defaultdict(lambda: 0)
        for f in feedbacks:
            if f["factor"]:
                res[f["factor"]["category"]] += 1
        return cls(result=[GroupStatItem(category=f, voted=v) for f, v in res.items()])


class ParticipantStatItem(BaseModel):
    date: datetime.date
    morning: State | None = None
    evening: State | None = None


class ParticipantStatResponse(BaseModel):
    result: list[ParticipantStatItem]

    @classmethod
    def from_feedbacks(cls, feedbacks: Sequence[Feedback]):
        res = {}
        for f in feedbacks:
            if f["date"] not in res:
                res[f["date"]] = ParticipantStatItem(date=f["date"])
            if f["day_time"] == DayTime.morning:
                res[f["date"]].morning = f["state"]
            if f["day_time"] == DayTime.evening:
                res[f["date"]].evening = f["state"]

        return cls(result=list(res.values()))
