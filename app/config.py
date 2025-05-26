from typing import Any

from pydantic_settings import BaseSettings
from pymongo import MongoClient


class Settings(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    SECRET: str

    DB_URL: str

    class Config():
        env_file='.env'


# environmental variables
env = Settings()

# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "API",
}