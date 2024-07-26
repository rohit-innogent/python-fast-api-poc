import logging
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schema.adhar import AdharResponse, AdharCreate
from app.service import adhar_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_adhar", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_adhar(adhar: AdharCreate, db: Session = Depends(get_db)):
    try:
        adhar_service.create_adhar(db, adhar)
        return "Adhar created successfully"
    except Exception as ex:
        logger.error(f"Error while creating adhar: {ex}")
        raise HTTPException(status_code=500, detail="Error creating adhar")


@router.get("/get_all_adhar", response_model=List[AdharResponse], status_code=status.HTTP_200_OK)
async def get_all_adhar(db: Session = Depends(get_db)):
    try:
        return adhar_service.get_all_adhar(db)
    except Exception as ex:
        logger.error(f"Error while retrieving all adhar: {ex}")
        raise HTTPException(status_code=500, detail="Error while retrieving all adhar")
