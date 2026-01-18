from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # .env
    DB_URL: str

    @field_validator("DB_URL")
    @classmethod
    def fix_db_url(cls, url: str | None) -> str:
        if not url:
            return ""

        return url.replace("postgres://", "postgresql+asyncpg://")


settings = Settings()
