from typing import TypedDict
import datetime
from .contracts import IdentifierType, UserRole, FactorType, DayTime


class Company(TypedDict):
    id: IdentifierType
    name: str


class BusinessUnit(TypedDict):
    id: IdentifierType
    name: str
    company: Company


class User(TypedDict):
    id: IdentifierType
    phone: str
    email: str
    permissions: list[str]
    password: bytes
    salt: bytes

    first_name: str
    last_name: str
    surname: str | None
    birthdate: datetime.date
    position: str
    business_unit: BusinessUnit
    role: UserRole | None


class Factor(TypedDict):
    id: IdentifierType
    name: str
    type: FactorType


class Category(TypedDict):
    id: IdentifierType
    name: str
    factors: list[Factor]


class State(TypedDict):
    id: IdentifierType
    name: str
    value: int


class FeedbackFactor(TypedDict):
    id: int
    name: int
    value: str | None


class Feedback(TypedDict):
    user_id: IdentifierType
    date: datetime.date
    day_time: DayTime
    state: State
    factor: FeedbackFactor | None
