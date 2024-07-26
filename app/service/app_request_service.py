import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.model import Adhar, AppRequest
from app.schema.adhar import AdharCreate
from app.schema.app_request import AppRequestCreate

logger = logging.getLogger(__name__)


def create_app_request(db: Session, app_request: AppRequestCreate):
    # post_obj = Post(**post.model_dump())
    try:
        app_request_obj = AppRequest(**app_request.model_dump())
        db.add(app_request_obj)
        db.commit()
        db.refresh(app_request_obj)
        logger.info(f"App request created successfully")
        return app_request_obj
    except Exception as ex:
        logger.error(f"Error creating app request: {ex}")
        db.rollback()
        raise


def get_all_app_request(db: Session):
    try:
        logger.info(f"Retrieving all app request from db")
        # return db.query(AppRequest).options(joinedload(AppRequest.app)).all()
        return db.query(AppRequest).all()

    except Exception as ex:
        logger.error(f"Error creating adhar: {ex}")
        db.rollback()
        raise


def delete_app_request(db: Session, app_request_id: int):
    try:
        # Find the app request object by ID
        app_request_obj = db.query(AppRequest).filter(AppRequest.id == app_request_id).first()

        if not app_request_obj:
            logger.error(f"App request with ID {app_request_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App request not found")

        # Delete the app request object
        db.delete(app_request_obj)
        db.commit()
        logger.info(f"App request with ID {app_request_id} deleted successfully")
        return {"detail": "App request deleted successfully"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        logger.error(f"Error deleting app request: {ex}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting app request")
