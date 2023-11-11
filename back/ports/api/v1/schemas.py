from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel, field_validator
import datetime
from domain.contracts import IdentifierType, DayTime
from domain.entities import User, Feedback


class MorningBody(BaseModel):
    state_id: IdentifierType


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None = None


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
    personal_data_confirmed: bool

    @field_validator("personal_data_confirmed")
    @classmethod
    def personal_data_confirmed_validator(cls, v: bool) -> bool:
        if not v:
            raise ValueError("personal_data_confirmed must be set to true")
        return v


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

    code: str | None

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
            code=user["code"],
        )


class ParticipantListResponse(BaseModel):
    result: list[Participant]


class ParticipantSingleResponse(BaseModel):
    result: Participant


class ManagerItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    department: str
    company: str


class ManagerResponse(BaseModel):
    result: ManagerItem


class RegistrationResponse(BaseModel):
    result: str


class RecommendationsResponse(BaseModel):
    result: str


class GroupFactor(BaseModel):
    id: IdentifierType
    name: str
    voted: int
    recommendation: str


class GroupStatItem(BaseModel):
    category: str
    factors: list[GroupFactor]


class GroupStatResponse(BaseModel):
    result: list[GroupStatItem]

    @classmethod
    def from_feedbacks(cls, feedbacks: Sequence[Feedback]):
        res = defaultdict(lambda: defaultdict(lambda: dict()))
        for f in feedbacks:
            if not f["factor"]:
                continue
            category = f["factor"]["category"]
            factor_id = f["factor"]["id"]
            recommendation = f["factor"]["manager_recommendation"]
            name = f["factor"]["name"]
            if factor_id not in res[category]:
                res[category][factor_id] = {
                    "recommendation": recommendation,
                    "name": name,
                    "id": factor_id,
                    "voted": 0,
                }
            res[category][factor_id]["voted"] += 1

        result = []
        for category in res:
            factors = []
            for factor_id in res[category]:
                factors.append(GroupFactor(**res[category][factor_id]))
            result.append(GroupStatItem(
                category=category,
                factors=factors,
            ))
        return cls(result=result)


class ParticipantFactor(BaseModel):
    id: IdentifierType
    name: str
    category: str
    recommendation: str


class ParticipantStatItem(BaseModel):
    date: datetime.date
    morning: State | None = None
    evening: State | None = None
    factor: ParticipantFactor | None = None


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
                if f["factor"]:
                    res[f["date"]].factor = ParticipantFactor(
                        id=f["factor"]["id"],
                        name=f["factor"]["name"],
                        category=f["factor"]["category"],
                        recommendation=f["factor"]["manager_recommendation"],
                    )

        return cls(result=list(res.values()))
