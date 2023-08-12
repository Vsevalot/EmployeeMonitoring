from typing import TypedDict
import datetime
from .contracts import IdentifierType


class Company(TypedDict):
    id: IdentifierType
    name: str


class BusinessUnit(TypedDict):
    id: IdentifierType
    name: str
    company: Company


class User(TypedDict):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    birthdate: datetime.date
    phone: str
    position: str
    email: str
    business_unit: BusinessUnit
    permissions: list[str]
