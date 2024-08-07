from typing import Type

from sqlalchemy.orm import Session

from app.models import App
from app.schemas.app import AppCreate


def create_app(db: Session, request_body: AppCreate) -> App:
    app_obj = App(**request_body.model_dump())
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj


def get_all_apps(db: Session) -> list[Type[App]]:
    return db.query(App).all()


def get_app_by_id(db: Session, app_id: int) -> Type[App] | None:
    return db.query(App).filter(App.id == app_id).first()


