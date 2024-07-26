import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.model import App, AppRequest
from app.schema.app import AppCreate

logger = logging.getLogger(__name__)


def create_app(db: Session, app: AppCreate):
    try:
        app_obj = App(**app.model_dump())
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)
        logger.info(f"App created successfully")
        return app_obj
    except Exception as ex:
        logger.error(f"Error creating App: {ex}")
        db.rollback()
        raise


def get_all_Apps(db: Session):
    try:
        logger.info(f"Retrieving all App from db")
        return db.query(App).all()
    except Exception as ex:
        logger.error(f"Error creating App: {ex}")
        db.rollback()
        raise


def delete_app(db: Session, app_id: int):
    try:
        # Find the app object by ID
        app_obj = db.query(App).filter(App.id == app_id).first()

        if not app_obj:
            logger.error(f"App with ID {app_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")

        # Find and delete all associated app requests
        associated_app_requests = db.query(AppRequest).filter(AppRequest.app_id == app_id).all()
        for app_request in associated_app_requests:
            db.delete(app_request)

        # Delete the app object
        db.delete(app_obj)
        db.commit()
        logger.info(f"App with ID {app_id} and all associated app requests deleted successfully")
        return {"detail": "App and associated app requests deleted successfully"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        logger.error(f"Error while deleting app: {ex}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting app")
