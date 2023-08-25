from fastapi import APIRouter, Depends

from ports.api.v1.schemas import ManagerRegisterBody, ParticipantRegisterBody, ManagerResponse
from services import TokenService, UserService
from ports.api.v1.dependencies import get_user_service, get_token_service


router = APIRouter(tags=["Registration"])


@router.post("/v1/register/managers")
async def register_manager(
    body: ManagerRegisterBody,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
) -> ManagerResponse:
    manager_id = await user_service.add_one_manager(data=body)
    token = await token_service.get_new_token(manager_id)
    return ManagerResponse(result=token)


@router.post("/v1/register/participants")
async def register_participant(
        body: ParticipantRegisterBody,
        user_service: UserService = Depends(get_user_service),
        token_service: TokenService = Depends(get_token_service),
) -> ManagerResponse:
    participant_id = await user_service.add_one_participant(data=body)
    token = await token_service.get_new_token(participant_id)
    return ManagerResponse(result=token)
