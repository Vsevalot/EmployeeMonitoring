from ports.api.v1.schemas import (
    ParticipantListResponse,
    Participant,
    ParticipantSingleResponse,
    GroupStatResponse,
    ParticipantStatResponse,
    RecommendationsResponse,
)
import datetime

from fastapi import APIRouter, Depends, HTTPException
from domain.entities import User
from domain.contracts import IdentifierType
from contracts import PARTICIPANT_READ_SELF
from services import UserService, FeedbackService
from ports.api.v1.dependencies import (
    get_current_user,
    get_user_service,
    get_feedback_service,
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


@router.get("/api/v1/participants/me/recommendations")
async def get_me(
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> RecommendationsResponse:
    recommendation = await feedback_service.get_user_recommendation(user_id=user["id"])
    return RecommendationsResponse(result=recommendation)


@router.get("/api/v1/participants/stats")
async def get_group_stat(
    date_from: datetime.date,
    date_to: datetime.date,
    feedback_service: FeedbackService = Depends(get_feedback_service),
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> GroupStatResponse:
    if PARTICIPANT_READ_SELF not in user["permissions"]:
        raise HTTPException(status_code=403)
    users = await user_service.get_list(
        {"organisation_unit_id": user["business_unit"]["id"]}
    )
    feedbacks = await feedback_service.get_list(
        filters={
            "date:ge": date_from,
            "date:le": date_to,
            "user_id:contains": [u["id"] for u in users],
        }
    )
    return GroupStatResponse.from_feedbacks(feedbacks)


@router.get("/api/v1/participants/{participant_id}")
async def get_participant(
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


@router.get("/api/v1/participants/{participant_id}/stats")
async def get_participants(
    participant_id: IdentifierType,
    date_from: datetime.date,
    date_to: datetime.date,
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> ParticipantStatResponse:
    if PARTICIPANT_READ_SELF not in user["permissions"]:
        raise HTTPException(status_code=403)
    users = await user_service.get_list(
        {"organisation_unit_id": user["business_unit"]["id"]}
    )
    if participant_id not in [u["id"] for u in users]:
        raise HTTPException(status_code=403)
    feedbacks = await feedback_service.get_list(
        filters={
            "user_id": participant_id,
            "date:ge": date_from,
            "date:le": date_to,
        }
    )
    return ParticipantStatResponse.from_feedbacks(feedbacks)
