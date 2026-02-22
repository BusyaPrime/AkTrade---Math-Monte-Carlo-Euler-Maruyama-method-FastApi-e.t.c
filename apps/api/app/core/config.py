from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AkTrade"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aktrade"
    REDIS_URL: str = "redis://localhost:6379/0"
    AKTRADE_SERVICE_KEY: str = "dev_service_key_change_me"

    class Config:
        env_file = ".env"

settings = Settings()
