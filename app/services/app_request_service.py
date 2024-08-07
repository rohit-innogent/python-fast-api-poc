import logging
from typing import Type

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.models import AppRequest
from app.schemas.app_request import AppRequestCreate, AppRequestUpdate
from app.repositories import app_request_repository

logger = logging.getLogger(__name__)


def create_app_request(db: Session, request_body: AppRequestCreate) -> dict:
    try:
        app_request_obj = app_request_repository.create_app_request(db, request_body)
        logger.info(f"App request created successfully: {app_request_obj.__dict__}")
        return {"detail": "App request created successfully"}
    except Exception as ex:
        db.rollback()
        raise ex


def get_all_app_request(db: Session) -> list[Type[AppRequest]]:
    logger.info(f"Retrieving all app request from db")
    return app_request_repository.get_all_app_request(db)


def delete_app_request(db: Session, app_request_id: int) -> dict:
    try:
        # Find the app request object by ID
        app_request_obj = app_request_repository.get_app_request_by_id(db, app_request_id)
        if not app_request_obj:
            logger.error(f"App request with ID {app_request_id} not found")
            raise NotFoundException(app_request_id)
        db.delete(app_request_obj)
        db.commit()
        logger.info(f"App request with ID {app_request_id} deleted successfully")
        return {"detail": "App request deleted successfully"}
    except NotFoundException as not_found_ex:
        raise not_found_ex
    except Exception as ex:
        db.rollback()
        raise ex


def update_app_request(db: Session, app_request_id: int, updated_app_request: AppRequestUpdate) -> dict:
    try:
        app_request_obj = app_request_repository.get_app_request_by_id(db, app_request_id)
        if not app_request_obj:
            logger.error(f"App request with ID {app_request_id} not found")
            raise NotFoundException(app_request_id)

        if updated_app_request.app_name:
            app_request_obj.app_name = updated_app_request.app_name
        db.commit()
        logger.info(f"App request with ID {app_request_id} updated successfully")
        return {"detail": "App request updated successfully"}
    except NotFoundException as not_found_ex:
        logger.error(f"App request with ID {app_request_id} not found during update")
        raise not_found_ex
    except Exception as ex:
        db.rollback()
        logger.error(f"Error while updating App request with ID {app_request_id}: {ex}")
        raise ex
