from pydantic import BaseModel
import datetime
from domain.contracts import IdentifierType, States, FactorType
from domain.entities import User


class MorningBody(BaseModel):
    state_id: IdentifierType


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None = None
    value: str | None = None


class FeedbackResponse(BaseModel):
    morning: States | None = None
    evening: States | None = None


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


class State(BaseModel):
    id: IdentifierType
    name: str
    value: int


class StatesResponse(BaseModel):
    res: list[State]


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
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            surname=user['surname'],
            phone=user['phone'],
            company=user['business_unit']['company']['name'],
            position=user['position'],
            email=user['email'],
            birthdate=user['birthdate'],
        )


class ParticipantListResponse(BaseModel):
    result: list[Participant]


class ParticipantSingleResponse(BaseModel):
    result: Participant


class Company(BaseModel):
    id: IdentifierType
    name: str


class Department(BaseModel):
    id: IdentifierType
    name: str
    company: Company


class ManagerListItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    department: Department


class ManagerListResponse(BaseModel):
    result: list[ManagerListItem]


class ManagerResponse(BaseModel):
    result: str


class RecommendationsResponse(BaseModel):
    result: str
