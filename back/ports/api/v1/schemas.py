from pydantic import BaseModel
import datetime
from domain.contracts import IdentifierType


class MorningBody(BaseModel):
    state_id: IdentifierType


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None


class FeedbackResponse(BaseModel):
    morning: bool
    evening: bool


class Factor(BaseModel):
    id: IdentifierType
    value: str


class FactorCategory(BaseModel):
    id: IdentifierType
    name: str
    factors: list[Factor]


class FactorsResponse(BaseModel):
    result: list[FactorCategory]


class InstructionResponse(BaseModel):
    result: str


class State(BaseModel):
    id: IdentifierType
    value: str


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


class EmployeeRegisterBody(RegisterBodyBase):
    manager_id: IdentifierType


class LoginBody(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    result: str


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
    result: list[ParticipantListItem]


class ManagerListItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    company: str
    department: str


class ManagerListResponse(BaseModel):
    result: list[ManagerListItem]
