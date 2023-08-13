from pydantic import BaseModel


class RegisterDTO(BaseModel):
    admin_login: str
    admin_password: str
    new_user_login: str
    new_user_password: str
