import logging

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.custom_exceptions.custom_exceptions import NotFoundException
from app.schemas.app import AppCreate, AppResponse
from app.services import app_service as app_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_app", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_app(app: AppCreate, db: Session = Depends(get_db)):
    try:
        return app_service.create_app(db, app)
    except Exception:
        raise HTTPException(status_code=500, detail="Error while creating app")


@router.get("/get_all_app", response_model=list[AppResponse], status_code=status.HTTP_200_OK)
async def get_all_app(db: Session = Depends(get_db)):
    try:
        return app_service.get_all_apps(db)
    except Exception as ex:
        logger.error(f"Error while retrieving all apps: {ex}")
        raise HTTPException(status_code=500, detail="Error while retrieving all apps")


@router.delete("/delete_app", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_app(app_id: int, db: Session = Depends(get_db)):
    try:
        return app_service.delete_app(db, app_id)
    except NotFoundException as ex:
        logger.error(f"App not found with app_id: {app_id}, while deleting app")
        raise ex
    except Exception as ex:
        logger.error(f"Error while deleting app: {ex}")
        raise HTTPException(status_code=500, detail="Error while deleting app")
