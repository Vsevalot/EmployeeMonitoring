from collections.abc import Sequence

from fastapi.responses import StreamingResponse

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
from domain.entities import User, Feedback
from domain.contracts import IdentifierType, DayTime
from contracts import PARTICIPANT_READ_ORGANISATION
from services import UserService, FeedbackService
from ports.api.v1.dependencies import (
    get_current_user,
    get_user_service,
    get_feedback_service,
)
from urllib.parse import quote

router = APIRouter(tags=["Participants"])


@router.get("/api/v1/participants")
async def get_participants(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ParticipantListResponse:
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
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
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
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


def _get_group_csv(feedbacks: Sequence[Feedback]) -> str:
    res = ["Фактор,Количество упоминаний"]
    factors = {}
    for f in feedbacks:
        factor = f['factor']
        if not factor:
            continue
        if factor['name'] not in factors:
            factors[factor['name']] = 0
        factors[factor['name']] += 1
    for f, num in factors.items():
        res.append(f'"{f}",{num}')
    return "\n".join(res)


@router.get("/api/v1/participants/stats/download-csv")
async def get_grop_stat_csv(
        date_from: datetime.date,
        date_to: datetime.date,
        feedback_service: FeedbackService = Depends(get_feedback_service),
        user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
) -> StreamingResponse:
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
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
    media_type = "text/csv"
    headers = {
        "Content-Disposition": f"attachment; filename*=utf-8''{date_from}-{date_to}.csv",
        "Content-Type": media_type,
    }
    csv_content = _get_group_csv(feedbacks)

    return StreamingResponse(
        content=iter(csv_content),
        headers=headers,
        media_type=media_type
    )


@router.get("/api/v1/participants/{participant_id}")
async def get_participant(
    participant_id: IdentifierType,
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> ParticipantSingleResponse:
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
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
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
        raise HTTPException(status_code=403)
    users = await user_service.get_list(
        {"organisation_unit_id": user["business_unit"]["id"]}
    )
    if participant_id not in [u["id"] for u in users]:
        raise HTTPException(status_code=403)
    feedback_range = await feedback_service.get_range(
        date_from=date_from,
        date_to=date_to,
        user_id=participant_id,
    )
    return ParticipantStatResponse.from_feedback_range(feedback_range)


def _csv_from_feedback_range(
        feedback_range: dict[datetime.date, dict[DayTime, Feedback | None]],
) -> str:
    res = ["Дата,Утро,Вечер,Категория ухудшения,Фактор ухудшения"]
    for date in feedback_range:
        morning = ""
        if feedback := feedback_range[date][DayTime.morning]:
            morning = feedback['state'].name
        evening = ""
        category = ""
        factor = ""
        if feedback := feedback_range[date][DayTime.evening]:
            evening = feedback['state'].name
            if _factor := feedback_range[date][DayTime.evening]["factor"]:
                factor = _factor["name"]
                category = _factor["category"]
        res.append(f"{date},{morning},{evening},{category},{factor}")
    return "\n".join(res)


@router.get("/api/v1/participants/{participant_id}/stats/download-csv")
async def get_single_stat_csv(
        participant_id: IdentifierType,
        date_from: datetime.date,
        date_to: datetime.date,
        user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
        feedback_service: FeedbackService = Depends(get_feedback_service),
) -> StreamingResponse:
    if PARTICIPANT_READ_ORGANISATION not in user["permissions"]:
        raise HTTPException(status_code=403)
    users = await user_service.get_list(
        {"organisation_unit_id": user["business_unit"]["id"]}
    )
    if participant_id not in [u["id"] for u in users]:
        raise HTTPException(status_code=403)
    feedback_range = await feedback_service.get_range(
        date_from=date_from,
        date_to=date_to,
        user_id=participant_id,
    )

    participant = await user_service.get_user(user_id=participant_id)
    media_type = "text/csv"
    filename = f"{participant['last_name']}-{date_from}-{date_to}.csv"
    encoded_filename = quote(filename.encode('utf-8'))
    headers = {
        "Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}",
        "Content-Type": media_type,
    }
    csv_content = _csv_from_feedback_range(feedback_range)

    return StreamingResponse(
        content=iter(csv_content),
        headers=headers,
        media_type=media_type
    )
