import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.profiles.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

logger.info(f"Database URL: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
