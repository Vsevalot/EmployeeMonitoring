import datetime
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from config import NOT_ENOUGH_FEEDBACKS_RECOMMENDATION, PERSONAL_RECOMMENDATION_MIN_FEEDBACKS
from domain.entities import Feedback
from domain.contracts import IdentifierType, DayTime
from utils import UnitOfWorkRDBS


class FeedbackService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_list(self, filters: Mapping[str:Any]) -> list[Feedback]:
        async with self._uow:
            return await self._uow.feedback.get_list(filters)

    async def get_user_recommendation(self, user_id: IdentifierType) -> str:
        month_back = datetime.date.today() - datetime.timedelta(days=30)
        async with self._uow:
            feedbacks = await self._uow.feedback.get_list(
                {
                    "date:ge": month_back,
                    "user_id": user_id,
                }
            )
        if not feedbacks or len(feedbacks) < PERSONAL_RECOMMENDATION_MIN_FEEDBACKS:
            return NOT_ENOUGH_FEEDBACKS_RECOMMENDATION
        recommendations = defaultdict(lambda: 0)
        for f in feedbacks:
            if not f["factor"]:
                continue
            recommendation = f["factor"]["personal_recommendation"]
            recommendations[recommendation] += 1
        if not recommendations:
            return NOT_ENOUGH_FEEDBACKS_RECOMMENDATION
        most_frequent, *_ = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return most_frequent[0]

    async def save(
        self,
        user_id: IdentifierType,
        date: datetime.date,
        state_id: IdentifierType,
        day_time: DayTime,
        factor_id: IdentifierType | None = None,
    ) -> None:
        async with self._uow:
            await self._uow.feedback.save(
                user_id=user_id,
                date=date,
                state_id=state_id,
                day_time=day_time,
                factor_id=factor_id,
            )
            await self._uow.commit()
