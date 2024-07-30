import logging

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.aadhar import AdharResponse, AdharCreate
from app.services import aadhar_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_aadhar", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_aadhar(adhar: AdharCreate, db: Session = Depends(get_db)):
    try:
        return aadhar_service.create_adhar(db, adhar)
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Error creating aadhar")


@router.get("/get_all_aadhar", response_model=list[AdharResponse], status_code=status.HTTP_200_OK)
async def get_all_aadhar(db: Session = Depends(get_db)):
    try:
        return aadhar_service.get_all_adhar(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Error while retrieving all aadhar")
