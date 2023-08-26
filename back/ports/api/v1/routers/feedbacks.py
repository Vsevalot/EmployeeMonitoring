import datetime

from fastapi import APIRouter, Depends, Response
from domain.entities import User
from ports.api.v1.schemas import FeedbackResponse, MorningBody, EveningBody
from domain.contracts import DayTime
from services import FeedbackService
from ports.api.v1.dependencies import (
    get_current_user,
    get_feedback_service,
)

router = APIRouter(tags=["Feedbacks"])


@router.get("/api/v1/feedbacks/{date}")
async def get_date_feedback(
    date: datetime.date,
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    feedbacks = await feedback_service.get_list(
        filters={"user_id": user["id"], "date": date}
    )
    feedbacks = {f["day_time"]: f["state"] for f in feedbacks}
    return FeedbackResponse.from_feedbacks(feedbacks)


@router.post("/api/v1/feedbacks/{date}/morning")
async def save_morning(
    date: datetime.date,
    body: MorningBody,
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> Response:
    await feedback_service.save(
        user_id=user["id"],
        state_id=body.state_id,
        date=date,
        day_time=DayTime.morning,
    )
    return Response(status_code=204)


@router.post("/api/v1/feedbacks/{date}/evening")
async def save_evening(
    date: datetime.date,
    body: EveningBody,
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> Response:
    await feedback_service.save(
        user_id=user["id"],
        state_id=body.state_id,
        date=date,
        day_time=DayTime.evening,
        factor_id=body.factor_id,
        value=body.value,
    )
    return Response(status_code=204)
