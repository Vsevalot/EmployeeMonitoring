from ports.api.v1.schemas import LoginResponse, LoginBody
from fastapi import APIRouter, Depends, HTTPException

from services import TokenService, UserService, PasswordService
from ports.api.v1.dependencies import get_user_service, get_token_service
from repositories.common import NotFoundError


router = APIRouter(tags=["Login"])


@router.post("/api/v1/login")
async def login_user(
    body: LoginBody,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
) -> LoginResponse:
    try:
        user = await user_service.get_user(email=body.email)
    except NotFoundError:
        raise HTTPException(status_code=401)

    pwd, salt = PasswordService.hash_password(body.password, salt=user['salt'])
    if pwd != user['password']:
        raise HTTPException(status_code=401)

    token = await token_service.get_new_token(user_id=user['id'])
    return LoginResponse(result=token)
