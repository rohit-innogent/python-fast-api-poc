import logging
from typing import Type

from sqlalchemy.orm import Session

from app.models import Role
from app.repositories import role_repository
from app.schemas.role import RoleCreate

logger = logging.getLogger(__name__)


def create_role(db: Session, request_body: RoleCreate) -> dict:
    try:
        role_obj = role_repository.create_role(db, request_body)
        logger.info(f"Role created successfully with role_id: {role_obj.id}")
        return {"detail": "Role created successfully"}
    except Exception as ex:
        logger.error(f"Error while creating role: {ex}")
        db.rollback()
        raise


def get_all_roles(db: Session) -> list[Type[Role]]:
    logger.info("Retrieving all roles from the database")
    return role_repository.get_all_roles(db)
