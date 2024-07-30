from typing import Type

from sqlalchemy.orm import Session

from app.models import AppRequest
from app.schemas.app_request import AppRequestCreate


def create_app_request(db: Session, request_body: AppRequestCreate) -> AppRequest:
    app_request_obj = AppRequest(**request_body.model_dump())
    db.add(app_request_obj)
    db.commit()
    db.refresh(app_request_obj)
    return app_request_obj


def get_app_requests_by_app_id(db: Session, app_id: int) -> list[Type[AppRequest]]:
    return db.query(AppRequest).filter(AppRequest.app_id == app_id).all()


def get_all_app_request(db: Session) -> list[Type[AppRequest]]:
    return db.query(AppRequest).all()


def get_app_request_by_id(db: Session, app_request_id) -> Type[AppRequest] | None:
    return db.query(AppRequest).filter(AppRequest.id == app_request_id).first()
