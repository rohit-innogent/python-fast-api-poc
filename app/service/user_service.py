import logging

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.model import Role
from app.model.user import User
from app.schema.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, user_request: UserCreate):
    try:
        # user_obj = User(**user.model_dump())
        user_obj = User(**user_request.model_dump(exclude={"roles"}))
        if user_request.roles:
            # Fetch roles from the database based on the provided role names
            roles = db.query(Role).filter(Role.role_name.in_(user_request.roles)).all()
            logger.info(f"following logs fetched: {roles}")
            user_obj.roles.extend(roles)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        logger.info(f"User created successfully with email: {user_obj.email}")
    except Exception as ex:
        logger.error(f"Error creating user: {ex}")
        db.rollback()  # Roll back the transaction in case of error
        raise


def get_user(user_id: int, db: Session):
    try:
        logger.info(f"Retrieving user from database with user_id: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            logger.warning(f"User with user_id {user_id} not found")
        return user
    except Exception as ex:
        logger.error(f"Error retrieving user with user_id {user_id}: {ex}")
        raise


def get_all_users(db: Session, limit: int = 10, offset: int = 0, direction: str = "asc"):
    try:
        logger.info(f"Retrieving users from the database with limit: {limit}, offset: {offset}, and direction: {direction}")
        # Default to ordering by 'id'
        order_column = getattr(User, 'id')

        # Determine the order direction
        order = desc(order_column) if direction == "desc" else asc(order_column)

        users = db.query(User).order_by(order).limit(limit).offset(offset).all()
        return users
    except Exception as e:
        logger.error(f"Error occurred while retrieving users: {e}")
        raise
