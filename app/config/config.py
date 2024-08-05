import logging
from logging.config import dictConfig

from pydantic_settings import BaseSettings
from app.config.logging.db_logging_config import DB_LOGGING_CONFIG

dictConfig(DB_LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str

    class Config:
        env_file = ".env.local"


settings = Settings()

logger.info(f"Active Environment - {settings.ENV}")
logger.info(f"Database URL - {settings.DATABASE_URL}")
