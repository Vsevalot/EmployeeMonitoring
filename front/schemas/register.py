from pydantic import BaseModel


class ManagerRegisterDTO(BaseModel):
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


class ManagerLinkDTO(BaseModel):
    link: str
