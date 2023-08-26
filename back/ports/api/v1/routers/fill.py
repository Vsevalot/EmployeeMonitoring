from pydantic import BaseModel

from ports.api.v1.definitions import Request
import datetime

from fastapi import APIRouter
from feed_db import get_random_feedbacks
from ports.rdbs.generic import feedback

router = APIRouter(tags=["Fill db with random feedbacks"])


class RandomFeedBody(BaseModel):
    user_id: int
    date_from: datetime.date
    date_to: datetime.date


@router.post("/api/v1/generate-random-feedbacks")
async def generate_random_feedbacks(
        request: Request,
        body: RandomFeedBody,
):
    feedbacks = get_random_feedbacks(body.user_id, body.date_from, body.date_to)
    async with request.app.engine.connect() as connection:
        stmt = feedback.insert().values(feedbacks)
        await connection.execute(stmt)
        await connection.commit()
