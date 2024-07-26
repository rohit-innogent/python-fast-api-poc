import logging
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schema.app_request import AppRequestCreate, AppRequestResponse
from app.service import app_request_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_app_request", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_app_request(app_request: AppRequestCreate, db: Session = Depends(get_db)):
    try:
        app_request_service.create_app_request(db, app_request)
        return "App request created successfully"
    except Exception as ex:
        logger.error(f"Error while creating app request: {ex}")
        raise HTTPException(status_code=500, detail="Error creating app request")


@router.get("/get_all_app_request", response_model=List[AppRequestResponse], status_code=status.HTTP_200_OK)
async def get_all_app_request(db: Session = Depends(get_db)):
    try:

        db_app_requests = app_request_service.get_all_app_request(db)
        return db_app_requests
    except Exception as ex:
        logger.error(f"Error while retrieving all app request: {ex}")
        raise HTTPException(status_code=500, detail="Error while retrieving all app request")


@router.delete("/delete_app_request", response_model=str, status_code=status.HTTP_200_OK)
async def delete_app_request(app_request_id: int, db: Session = Depends(get_db)):
    try:
        app_request_service.delete_app_request(db, app_request_id)
        return "App request deleted successfully"
    except HTTPException as htt_exp:
        raise htt_exp
    except Exception as ex:
        logger.error(f"Error while creating app request: {ex}")
        raise HTTPException(status_code=500, detail="Error creating app request")