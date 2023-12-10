from services.password import PasswordService
from utils import UnitOfWorkRDBS

from fastapi import Depends, HTTPException

from services.token import TokenService
from services.user import UserService
from services.category import CategoryService
from services.state import StateService
from services.feedback import FeedbackService
from services.device import DeviceService
from domain.entities import User

from .definitions import Request


async def get_user_service(request: Request) -> UserService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return UserService(uow=uow, password_service=PasswordService())


async def get_token_service(request: Request) -> TokenService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return TokenService(uow=uow)


async def get_category_service(request: Request) -> CategoryService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return CategoryService(uow=uow)


async def get_state_service(request: Request) -> StateService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return StateService(uow=uow)


async def get_feedback_service(request: Request) -> FeedbackService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return FeedbackService(uow=uow)


async def get_current_user(
    request: Request,
    token_service: TokenService = Depends(get_token_service),
    user_service: UserService = Depends(get_user_service),
) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401)

    user_id = await token_service.get_user_id(token)
    if not user_id:
        raise HTTPException(status_code=401)
    return await user_service.get_user(user_id)


async def get_device_service(request: Request) -> DeviceService:
    uow = UnitOfWorkRDBS(connection_fabric=request.app.engine)
    return DeviceService(uow)
