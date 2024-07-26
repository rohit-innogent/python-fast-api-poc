import logging
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schema.app import AppCreate, AppResponse
from app.service import app_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_app", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_app(app: AppCreate, db: Session = Depends(get_db)):
    try:
        app_service.create_app(db, app)
        return "App created successfully"
    except Exception as ex:
        logger.error(f"Error while creating app: {ex}")
        raise HTTPException(status_code=500, detail="Error creating app")


@router.get("/get_all_app", response_model=List[AppResponse], status_code=status.HTTP_200_OK)
async def get_all_app(db: Session = Depends(get_db)):
    try:
        apps = app_service.get_all_Apps(db)
        for index, app_request in enumerate(apps):
            print(f"Object {index + 1}: {app_request.__dict__}")
        return apps
    except Exception as ex:
        logger.error(f"Error while retrieving all app: {ex}")
        raise HTTPException(status_code=500, detail="Error while retrieving all app")


@router.delete("/delete_app", response_model=str, status_code=status.HTTP_201_CREATED)
async def delete_app(app_id: int, db: Session = Depends(get_db)):
    try:
        app_service.delete_app(db, app_id)
        return "App deleted successfully"
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        logger.error(f"Error while creating app: {ex}")
        raise HTTPException(status_code=500, detail="Error deleting app")
