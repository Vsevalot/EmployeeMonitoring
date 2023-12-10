from pydantic import BaseModel

from ports.api.v1.definitions import Request

from fastapi import APIRouter
from ports.rdbs.generic import feedback
import datetime
import random

from domain.entities import State
from domain.contracts import DayTime


MORNING_STATES = (
    State(3, "Good", 300),
    State(3, "Good", 300),
    State(3, "Good", 300),
    State(2, "Average", 200),
    State(2, "Average", 200),
    State(1, "Bad", 100),
)
EVENING_STATES = (
    State(3, "Good", 300),
    State(2, "Average", 200),
    State(2, "Average", 200),
    State(1, "Bad", 100),
    State(1, "Bad", 100),
    State(1, "Bad", 100),
)


def get_random_feedbacks(
    user_id: int, start_date: datetime.date, end_date: datetime.date
):
    to_insert = []
    delta = end_date - start_date
    for d in range(delta.days + 1):
        date = start_date + datetime.timedelta(days=d)
        morning = random.choice(MORNING_STATES)
        evening = random.choice(EVENING_STATES)
        bad_factor = None
        if evening < morning:
            bad_factor = random.randint(1, 20)
        to_insert.append(
            {
                "date": date,
                "user_id": user_id,
                "day_time": DayTime.morning.value,
                "state_id": morning.id,
                "factor_id": None,
            }
        )
        to_insert.append(
            {
                "date": date,
                "user_id": user_id,
                "day_time": DayTime.evening.value,
                "state_id": evening.id,
                "factor_id": bad_factor,
            }
        )
    return to_insert


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
