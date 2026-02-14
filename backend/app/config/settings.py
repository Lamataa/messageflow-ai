from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):

    APP_NAME: str = "MessageFlow AI"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str = "postgresql://messageflow:messageflow123@localhost:5432/messageflow_db"

    REDIS_URL: str = "redis://localhost:6379/0"

    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/"

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

settings = Settings()