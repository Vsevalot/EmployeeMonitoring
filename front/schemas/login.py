from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    email: str
    password: str


class LoginResponseDTO(BaseModel):
    res: str
