from ports.api.v1.schemas import (
    ParticipantListResponse,
    Participant,
    ParticipantSingleResponse,
)
import datetime

from fastapi import APIRouter, Depends, HTTPException
from domain.entities import User
from domain.contracts import IdentifierType
from contracts import PARTICIPANT_READ_SELF
from services import UserService
from ports.api.v1.dependencies import (
    get_current_user,
    get_user_service,
)


router = APIRouter(tags=["Participants"])


@router.get("/api/v1/participants")
async def get_participants(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ParticipantListResponse:
    if PARTICIPANT_READ_SELF not in user["permissions"]:
        raise HTTPException(status_code=403)
    users = await user_service.get_list(
        {"organisation_unit_id": user["business_unit"]["id"]}
    )
    return ParticipantListResponse(result=[Participant.from_user(u) for u in users])


@router.get("/api/v1/participants/me")
async def get_me(
    user: User = Depends(get_current_user),
) -> ParticipantSingleResponse:
    return ParticipantSingleResponse(result=Participant.from_user(user))


@router.get("/api/v1/participants/{participant_id}")
async def get_me(
    participant_id: IdentifierType,
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ParticipantSingleResponse:
    if PARTICIPANT_READ_SELF not in user["permissions"]:
        raise HTTPException(status_code=403)
    requested_users = await user_service.get_list(
        {
            "id": participant_id,
            "organisation_unit_id": user["business_unit"]["id"],
        }
    )
    if not requested_users:
        raise HTTPException(status_code=404)
    return ParticipantSingleResponse(result=Participant.from_user(requested_users[0]))

#
# @router.get("/api/v1/participants/:id/stats")
# async def get_participants(
#     date_from: datetime.date,
#     date_to: datetime.date,
#     user: User = Depends(get_current_user),
#     user_service: UserService = Depends(get_user_service),
# ) -> ParticipantListResponse:
#     if PARTICIPANT_READ_SELF not in user["permissions"]:
#         raise HTTPException(status_code=403)
#     users = await user_service.get_list(
#         {"organisation_unit_id": user["business_unit"]["id"]}
#     )
#     return list[DateFeedback]
#     return ParticipantListResponse(result=[Participant.from_user(u) for u in users])
#
#
# @router.get("/api/v1/participants/stats")
# async def get_participants(
#         date_from: datetime.date,
#         date_to: datetime.date,
#         user: User = Depends(get_current_user),
#         user_service: UserService = Depends(get_user_service),
# ) -> ParticipantListResponse:
#     if PARTICIPANT_READ_SELF not in user["permissions"]:
#         raise HTTPException(status_code=403)
#     users = await user_service.get_list(
#         {"organisation_unit_id": user["business_unit"]["id"]}
#     )
#     return {"nachalstvo": 23}
#     return ParticipantListResponse(result=[Participant.from_user(u) for u in users])
#
