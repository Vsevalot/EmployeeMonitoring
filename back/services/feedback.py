import datetime
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from config import (
    NOT_ENOUGH_FEEDBACKS_RECOMMENDATION,
    PERSONAL_RECOMMENDATION_MIN_FEEDBACKS,
)
from domain.entities import Feedback
from domain.contracts import IdentifierType, DayTime
from utils import UnitOfWorkRDBS


class ApproximationError(Exception):
    ...


class FeedbackService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_list(self, filters: Mapping[str:Any]) -> list[Feedback]:
        async with self._uow:
            return await self._uow.feedback.get_list(filters)

    async def get_range(
        self,
        date_from: datetime.date,
        date_to: datetime.date,
        user_id: IdentifierType,
    ) -> dict[datetime.date, dict[DayTime, Feedback | None]]:
        filters = {
            "user_id": user_id,
            "date:ge": date_from,
            "date:le": date_to,
        }
        async with self._uow:
            feedbacks = await self._uow.feedback.get_list(filters)
        feedback_range = [
            {DayTime.morning: None, DayTime.evening: None}
            for _ in range((date_to - date_from).days + 1)
        ]
        feedback_date_range = {
            date_from + datetime.timedelta(days=d): d
            for d in range((date_to - date_from).days + 1)
        }
        for f in feedbacks:
            date_position = feedback_date_range[f['date']]
            feedback_range[date_position][f["day_time"]] = f

        try:
            for i in range(len(feedback_range)):
                morning = feedback_range[i][DayTime.morning]
                evening = feedback_range[i][DayTime.evening]
                if morning is None:
                    self._approximate(
                        current_index=i,
                        feedback_range=feedback_range,
                        day_time=DayTime.morning,
                    )
                if evening is None:
                    self._approximate(
                        current_index=i,
                        feedback_range=feedback_range,
                        day_time=DayTime.evening,
                    )
        except ApproximationError:
            return {date: feedbacks for date, feedbacks in zip(feedback_date_range, feedback_range)}
        return {date: feedbacks for date, feedbacks in zip(feedback_date_range, feedback_range)}

    def _approximate(
            self,
            current_index: int,
            feedback_range: list[dict[DayTime, Feedback | None]],
            day_time: DayTime,
    ):
        if current_index == 0 or feedback_range[current_index - 1][day_time] is None:
            self._set_as_closest_in_the_future(
                current=current_index,
                feedback_range=feedback_range,
                day_time=day_time,
            )
        else:
            feedback_range[current_index][day_time] = feedback_range[current_index - 1][day_time]

    @staticmethod
    def _set_as_closest_in_the_future(
        current: int,
        feedback_range: list[dict[DayTime, Feedback | None]],
        day_time: DayTime,
    ) -> None:
        for i in range(current + 1, len(feedback_range)):
            feedback = feedback_range[i][day_time]
            if feedback:
                for k in range(current, i):
                    feedback_range[k][day_time] = feedback
                return
        raise ApproximationError("Can't calculate the value of feedback")

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
        most_frequent, *_ = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True,
        )
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
