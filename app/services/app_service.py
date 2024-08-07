import logging

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.repositories import app_repository as app_repo, app_request_repository as app_request_repo
from app.schemas.app import AppCreate

logger = logging.getLogger(__name__)


def create_app(db: Session, request_body: AppCreate) -> dict:
    try:
        app = app_repo.create_app(db, request_body)
        logger.info(f"App created successfully: {app.__dict__}")
        return {"detail": "App created successfully"}
    except Exception as ex:
        logger.error(f"Error while creating App: {ex}")
        db.rollback()
        raise


def get_all_apps(db: Session):
    logger.info(f"Retrieving all App from db")
    return app_repo.get_all_apps(db)


def delete_app(db: Session, app_id: int):
    try:
        app_obj = app_repo.get_app_by_id(db, app_id)
        if not app_obj:
            logger.error(f"App with ID {app_id} not found")
            raise NotFoundException(app_id)

        associated_app_requests = app_request_repo.get_app_requests_by_app_id(db, app_id)
        for app_request in associated_app_requests:
            db.delete(app_request)

        db.delete(app_obj)
        db.commit()
        logger.info(f"App with ID {app_id} and all associated app requests deleted successfully")
        return {"detail": "App and associated app requests deleted successfully"}
    except NotFoundException as ex:
        raise ex
    except Exception as ex:
        db.rollback()
        raise ex
