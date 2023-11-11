from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select
from domain.entities import Factor, Category
from domain.contracts import FactorType
from ports.rdbs.generic import factor, category


class CategoryRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def get_list(self) -> list[Category]:
        joined = factor.join(category, category.c.id == factor.c.category_id)
        stmt = select(
            factor.c.id,
            factor.c.name,
            factor.c.category_id,
            category.c.name.label("category_name"),
        ).select_from(joined)
        res = await self._connection.execute(stmt)
        res = res.fetchall()
        return self._get_categories(res)

    @staticmethod
    def _get_categories(rows) -> list[Category]:
        factor_by_categories = {}
        for r in rows:
            if r.category_id not in factor_by_categories:
                factor_by_categories[r.category_id] = []
            factor_by_categories[r.category_id].append(r)

        res = []

        for category_id, factors in factor_by_categories.items():
            res.append(
                Category(
                    id=category_id,
                    name=factors[0].category_name,
                    factors=[Factor(id=f.id, name=f.name) for f in factors],
                )
            )
        return res
