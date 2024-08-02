import logging
import os
from logging.config import dictConfig

from dotenv import load_dotenv

from app.config.logging.db_logging_config import DB_LOGGING_CONFIG

dictConfig(DB_LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# This will load all the values from .env to environment
load_dotenv()


def get_settings():
    # Here fetching EVN value from environment
    env = os.getenv("ENV")
    logger.info(f"Active environment: {env}")
    if env == "local":
        from .config_local import Settings
    elif env == "dev":
        from .config_dev import Settings
    else:
        raise ValueError(f"Unknown environment: {env}")
    return Settings()
