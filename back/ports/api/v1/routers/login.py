from fastapi import APIRouter

from ports.api.v1.schemas import LoginResponse, LoginBody


router = APIRouter(tags=["Login"])


@router.post("/v1/login")
async def login_user(
    body: LoginBody,
) -> LoginResponse:
    return LoginResponse(result="test")
