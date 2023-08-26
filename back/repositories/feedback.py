from collections.abc import Mapping
from typing import Any
import datetime

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from domain.entities import Feedback, FeedbackFactor, State
from domain.contracts import DayTime, IdentifierType
from ports.rdbs.generic import state, feedback, factor, category
from .common import AlreadyInUse, OPERATORS


class FeedbackRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def get_list(self, filters: Mapping[str, Any]) -> list[Feedback]:
        joined = feedback.join(state, feedback.c.state_id == state.c.id).join(
            factor, feedback.c.factor_id == factor.c.id, isouter=True
        ).join(category, factor.c.category_id == category.c.id, isouter=True)
        stmt = select(
            feedback.c.user_id,
            feedback.c.date,
            feedback.c.day_time,
            feedback.c.value,
            factor.c.id.label("factor_id"),
            factor.c.name.label("factor_name"),
            category.c.name.label("category_name"),
            state.c.id.label("state_id"),
            state.c.name.label("state_name"),
            state.c.value.label("state_value"),
        ).select_from(joined)
        if filters:
            stmt = self._apply_filters(stmt, filters)
        stmt = stmt.order_by(feedback.c.date, feedback.c.user_id, feedback.c.day_time)
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
        for col, value in filters.items():
            column, _, operation = col.partition(":")
            column = getattr(feedback.c, column)
            if not operation:
                operation = 'eq'
            operation = OPERATORS[operation]
            stmt = stmt.where(operation(column, value))
        return stmt

    @staticmethod
    def _get_feedback(row) -> Feedback:
        f = None
        if row.factor_id:
            f = FeedbackFactor(
                id=row.factor_id,
                name=row.factor_name,
                value=row.value,
                category=row.category_name,
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
