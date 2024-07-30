import logging
from typing import Type

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import UserNotFoundException
from app.models import User
from app.repositories import user_repository
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, request_body: UserCreate) -> dict:
    try:
        user_obj = user_repository.create_user(db, request_body)
        logger.info(f"User created successfully with email: {user_obj.email}")
        return {"details": "User created successfully"}
    except Exception as ex:
        logger.error(f"Error while creating user: {ex}")
        db.rollback()
        raise


def get_user_by_id(db: Session, user_id: int) -> Type[User]:
    logger.info(f"Retrieving user from database with user_id: {user_id}")
    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        logger.warning(f"User with user_id {user_id} not found")
        raise UserNotFoundException(user_id)
    return user


def get_all_users_with_pagination(db: Session, limit: int = 10, offset: int = 0, direction: str = "asc") -> list[Type[User]]:
    logger.info(f"Retrieving users from the database with limit: {limit}, offset: {offset}, and direction: {direction}")
    return user_repository.get_all_users_with_pagination(db, limit, offset, direction)
