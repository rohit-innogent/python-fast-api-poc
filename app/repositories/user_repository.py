from typing import Type

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import role_repository
from app.schemas.user import UserCreate


def create_user(db: Session, user_obj: User) -> User:
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def get_user_by_id(db: Session, user_id: int) -> Type[User] | None:
    return db.query(User).filter(User.id == user_id).first()


def get_all_users_with_pagination(db: Session, limit: int = 10, offset: int = 0, direction: str = "asc") -> list[Type[User]]:
    # Default to ordering by 'id'
    order_column = getattr(User, 'id')
    order = desc(order_column) if direction == "desc" else asc(order_column)
    return db.query(User).order_by(order).limit(limit).offset(offset).all()


def get_user_by_username(db: Session, username: str) -> Type[User] | None:
    return db.query(User).filter(User.username == username).first()
