from typing import Type

from sqlalchemy.orm import Session, joinedload

from app.models import Role
from app.schemas.role import RoleCreate


def create_role(db: Session, request_body: RoleCreate) -> Role:
    role_obj = Role(**request_body.model_dump())
    db.add(role_obj)
    db.commit()
    db.refresh(role_obj)
    return role_obj


def get_all_roles(db: Session) -> list[Type[Role]]:
    return db.query(Role).options(joinedload(Role.users)).all()


def get_roles_by_role_names(db: Session, requested_roles: list) -> list[Type[Role]]:
    return db.query(Role).filter(Role.role_name.in_(requested_roles)).all()
