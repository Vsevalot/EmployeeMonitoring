from fastapi import APIRouter, Depends

from ports.api.v1.schemas import ManagerRegisterBody, ParticipantRegisterBody, RegistrationResponse
from services import TokenService, UserService
from ports.api.v1.dependencies import get_user_service, get_token_service


router = APIRouter(tags=["Registration"])


@router.post("/api/v1/register/managers", status_code=201)
async def register_manager(
    body: ManagerRegisterBody,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
) -> RegistrationResponse:
    manager_id = await user_service.add_one_manager(data=body)
    token = await token_service.get_new_token(manager_id)
    return RegistrationResponse(result=token)


@router.post("/api/v1/register/participants", status_code=201)
async def register_participant(
        body: ParticipantRegisterBody,
        user_service: UserService = Depends(get_user_service),
        token_service: TokenService = Depends(get_token_service),
) -> RegistrationResponse:
    participant_id = await user_service.add_one_participant(data=body)
    token = await token_service.get_new_token(participant_id)
    return RegistrationResponse(result=token)
