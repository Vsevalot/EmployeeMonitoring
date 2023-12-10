from typing import TypedDict
import datetime
from .contracts import IdentifierType, UserRole, DayTime


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

    code: str


class Factor(TypedDict):
    id: IdentifierType
    name: str


class Category(TypedDict):
    id: IdentifierType
    name: str
    factors: list[Factor]


class State:
    def __init__(self, id: IdentifierType, name: str, value: int):
        self.id = id
        self.name = name
        self.value = value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return f'{self.name}'


class FeedbackFactor(TypedDict):
    id: int
    name: str
    category: str
    manager_recommendation: str
    personal_recommendation: str


class Feedback(TypedDict):
    user_id: IdentifierType
    date: datetime.date
    day_time: DayTime
    state: State
    factor: FeedbackFactor | None


class Device(TypedDict):
    id: str
    token: str
