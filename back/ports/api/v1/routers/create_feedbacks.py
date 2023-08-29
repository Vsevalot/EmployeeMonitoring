import asyncio
import datetime
import random

from sqlalchemy.ext.asyncio import create_async_engine
import pydantic_settings
from domain.entities import State
from domain.contracts import DayTime
from ports.rdbs.generic import feedback


class DBConfig(pydantic_settings.BaseSettings):
    password: str = "123"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    database: str = "monitoring"

    @property
    def dsn(self):
        dsn = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return dsn

    class Config:
        case_sensitive = False
        secrets_dir = "/run/secrets"
        env_prefix = "rdbs_"


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


def get_random_feedbacks(user_id: int, start_date: datetime.date, end_date: datetime.date):
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


async def main():
    start_date = datetime.date(2022, 5, 1)
    end_date = datetime.date(2022, 6, 3)
    user_id = 2
    to_insert = get_random_feedbacks(user_id=user_id, start_date=start_date, end_date=end_date)

    engine = create_async_engine(DBConfig().dsn)
    async with engine.connect() as connection:
        stmt = feedback.insert().values(to_insert)
        res = await connection.execute(stmt)
        await connection.commit()


asyncio.run(main())
