from typing import Type

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import role_repository
from app.schemas.user import UserCreate


def create_user(db: Session, request_body: UserCreate) -> User:
    user_obj = User(**request_body.model_dump(exclude={"roles"}))
    if request_body.roles:
        roles = role_repository.get_roles_by_role_names(db, request_body.roles)
        user_obj.roles.extend(roles)
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
