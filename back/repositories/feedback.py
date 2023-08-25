from collections.abc import Mapping
from operator import eq
from typing import Any
import datetime

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from domain.entities import Feedback, FeedbackFactor, State
from domain.contracts import DayTime, IdentifierType
from ports.rdbs.generic import state, feedback, factor
from .common import AlreadyInUse


class FeedbackRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def get_list(self, filters: Mapping[str, Any]) -> list[Feedback]:
        joined = feedback.join(state, feedback.c.state_id == state.c.id).join(
            factor, feedback.c.factor_id == factor.c.id, isouter=True
        )
        stmt = select(
            feedback.c.user_id,
            feedback.c.date,
            feedback.c.day_time,
            feedback.c.value,
            factor.c.id.label("factor_id"),
            factor.c.name.label("factor_name"),
            state.c.id.label("state_id"),
            state.c.name.label("state_name"),
            state.c.value.label("state_value"),
        ).select_from(joined)
        if filters:
            stmt = self._apply_filters(stmt, filters)
        res = await self._connection.execute(stmt)
        res = res.fetchall()
        return [self._get_feedback(r) for r in res]

    async def save(
        self,
        user_id: IdentifierType,
        date: datetime.date,
        state_id: IdentifierType,
        day_time: DayTime,
        factor_id: IdentifierType | None,
        value: str | None,
    ) -> None:
        stmt = feedback.insert().values(
            date=date,
            user_id=user_id,
            day_time=day_time.value,
            value=value,
            factor_id=factor_id,
            state_id=state_id,
        )
        try:
            await self._connection.execute(stmt)
        except IntegrityError:
            raise AlreadyInUse

    @staticmethod
    def _apply_filters(stmt, filters: Mapping[str, Any]):
        for column, value in filters.items():
            stmt = stmt.where(eq(getattr(feedback.c, column), value))
        return stmt

    @staticmethod
    def _get_feedback(row) -> Feedback:
        f = None
        if row.factor_id:
            f = FeedbackFactor(
                id=row.factor_id,
                name=row.factor_name,
                value=row.value,
            )
        return Feedback(
            user_id=row.user_id,
            date=row.date,
            day_time=DayTime(row.day_time),
            state=State(
                id=row.state_id,
                name=row.state_name,
                value=row.state_value,
            ),
            factor=f,
        )
