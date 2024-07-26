import logging

from sqlalchemy.orm import Session, joinedload

from app.model import Role
from app.schema.role import RoleCreate

logger = logging.getLogger(__name__)


def create_role(db: Session, role: RoleCreate):
    try:
        role_obj = Role(**role.model_dump())
        db.add(role_obj)
        db.commit()
        db.refresh(role_obj)
        logger.info(f"Role created successfully with role_id: {role_obj.id}")
    except Exception as ex:
        logger.error(f"Error while creating role: {ex}")
        db.rollback()
        raise


def get_all_roles(db: Session):
    try:
        logger.info("Retrieving all roles from the database")
        return db.query(Role).options(joinedload(Role.users)).all()
    except Exception as ex:
        logger.error(f"Error retrieving all roles: {ex}")
        raise
