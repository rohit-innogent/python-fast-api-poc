import logging

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.custom_exceptions.custom_exceptions import NotFoundException
from app.schemas.app_request import AppRequestCreate, AppRequestResponse, AppRequestUpdate
from app.services import app_request_service as app_request_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_app_request", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_app_request(app_request: AppRequestCreate, db: Session = Depends(get_db)):
    try:
        return app_request_service.create_app_request(db, app_request)
    except Exception as ex:
        logger.error(f"Error while creating app request: {ex}")
        raise HTTPException(status_code=500, detail="Error while creating app request")


@router.get("/get_all_app_request", response_model=list[AppRequestResponse], status_code=status.HTTP_200_OK)
async def get_all_app_request(db: Session = Depends(get_db)):
    try:
        return app_request_service.get_all_app_request(db)
    except Exception as ex:
        logger.error(f"Error while retrieving all app request: {ex}")
        raise HTTPException(status_code=500, detail="Error while retrieving all app request")


@router.delete("/delete_app_request", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_app_request(app_request_id: int, db: Session = Depends(get_db)):
    try:
        return app_request_service.delete_app_request(db, app_request_id)
    except NotFoundException as ex:
        raise ex
    except Exception as ex:
        logger.error(f"Error while deleting app request: {ex}")
        raise HTTPException(status_code=500, detail="Error while deleting app request")


@router.put("/update_app_request", response_model=None, status_code=status.HTTP_200_OK)
def update_app_request(app_request_id: int, updated_app_request: AppRequestUpdate, db: Session = Depends(get_db)):
    try:
        return app_request_service.update_app_request(db, app_request_id, updated_app_request)
    except NotFoundException as ex:
        raise ex
    except Exception as ex:
        logger.error(f"Error while updating app request: {ex}")
        raise HTTPException(status_code=500, detail="Error while updating app request")
