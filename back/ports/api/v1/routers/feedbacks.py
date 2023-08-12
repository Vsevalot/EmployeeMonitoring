from typing import Annotated
import datetime

from fastapi import APIRouter, Response, Header


from ports.api.v1.schemas import FeedbackResponse, MorningBody, EveningBody


router = APIRouter(tags=["Feedbacks"])


@router.get("/v1/feedbacks/{feedback_date}")
async def get_instruction(
    authorization: Annotated[str | None, Header()],
    feedback_date: datetime.date,
) -> FeedbackResponse:
    return FeedbackResponse(morning=False, evening=False)


@router.post("/v1/feedbacks/{feedback_date}/morning")
async def save_morning(
    authorization: Annotated[str | None, Header()],
    feedback_date: datetime.date,
    body: MorningBody,
) -> Response:
    return Response(status_code=201)


@router.post("/v1/feedbacks/{feedback_date}/evening")
async def save_evening(
    authorization: Annotated[str | None, Header()],
    feedback_date: datetime.date,
    body: EveningBody,
) -> Response:
    return Response(status_code=201)
