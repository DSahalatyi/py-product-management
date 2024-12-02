from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str | None = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
