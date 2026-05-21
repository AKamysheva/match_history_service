# flake8: noqa: E501
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST_DB: str
    PORT_DB: int
    API_RIOT_KEY: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.HOST_DB}:{self.PORT_DB}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
