import logging

from sqlalchemy.orm import Session, joinedload

from app.model import Adhar
from app.schema.adhar import AdharCreate

logger = logging.getLogger(__name__)


def create_adhar(db: Session, adhar: AdharCreate):
    # post_obj = Post(**post.model_dump())
    try:
        adhar_obj = Adhar(**adhar.model_dump())
        db.add(adhar_obj)
        db.commit()
        db.refresh(adhar_obj)
        logger.info(f"Adhar created successfully")
        return adhar_obj
    except Exception as ex:
        logger.error(f"Error creating adhar: {ex}")
        db.rollback()
        raise


def get_all_adhar(db: Session):
    try:
        logger.info(f"Retrieving all adhar from db")
        return db.query(Adhar).options(joinedload(Adhar.user)).all()
    except Exception as ex:
        logger.error(f"Error creating adhar: {ex}")
        db.rollback()
        raise
