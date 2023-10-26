import datetime
from collections.abc import Mapping
from typing import Any

from domain.entities import Feedback
from domain.contracts import IdentifierType, DayTime
from utils import UnitOfWorkRDBS


class FeedbackService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_list(self, filters: Mapping[str:Any]) -> list[Feedback]:
        async with self._uow:
            return await self._uow.feedback.get_list(filters)

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
