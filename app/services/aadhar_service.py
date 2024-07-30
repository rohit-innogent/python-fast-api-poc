import logging
from typing import Type

from sqlalchemy.orm import Session

from app.models import Adhar
from app.schemas.aadhar import AdharCreate
from app.repositories import aadhar_repository

logger = logging.getLogger(__name__)


def create_adhar(db: Session, request_body: AdharCreate) -> dict:
    try:
        aadhar_obj = Adhar(**request_body.model_dump())
        adhar_obj = aadhar_repository.create_aadhar(db, aadhar_obj)
        logger.info(f"Adhar created successfully: {adhar_obj.__dict__}")
        return {"detail": "Aadhar created successfully"}
    except Exception as ex:
        logger.error(f"Error while creating aadhar: {ex}")
        db.rollback()
        raise


def get_all_adhar(db: Session) -> list[Type[Adhar]]:
    try:
        logger.info(f"Retrieving all adhar from db")
        return aadhar_repository.get_all_adhar(db)
    except Exception as ex:
        logger.error(f"Error creating adhar: {ex}")
        db.rollback()
        raise
