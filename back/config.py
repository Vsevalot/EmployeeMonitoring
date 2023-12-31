from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    host: str
    port: int = 5432
    database: str
    user: str
    password: SecretStr = Field(..., env="rdbs_password")
    echo: bool = False

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}?async_fallback=True"

    class Config:
        case_sensitive = False
        env_file = ".env"
        secrets_dir = "/run/secrets"
        env_prefix = "rdbs_"


MANAGER_CODE_LENGTH = 5
NOT_ENOUGH_FEEDBACKS_RECOMMENDATION = (
    "Для получения персональных рекоммендаций необходимо "
    "проанализировать ваши ответы за последний месяц. "
    "Пожалуйста, продолжайте отмечать свое самочувствие в приложении."
)
PERSONAL_RECOMMENDATION_MIN_FEEDBACKS = 10
DAYS_FOR_GROUP_STAT = 30
