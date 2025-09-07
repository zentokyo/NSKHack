from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_prefix="POSTGRES_", extra="ignore")
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Config(BaseSettings):
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


config = Config()