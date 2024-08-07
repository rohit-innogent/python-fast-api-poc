from typing import Optional
from pydantic import BaseModel

from app.models import AppRequest

from app.models.app import App
from app.schemas.app import AppResponse


class AppRequestBase(BaseModel):
    app_name: str
    app_id: int


class AppRequestCreate(AppRequestBase):
    pass


class AppRequestUpdate(BaseModel):
    app_name: str


class AppRequestResponse(AppRequestBase):
    id: int
    app: Optional[AppResponse] = None

    class Config:
        from_attributes = True


def convert_app_to_dict(app_instance: App) -> dict:
    return {
        'app_name': app_instance.app_name,
        'app_desc': app_instance.app_desc,
        'id': app_instance.id
    }


def convert_app_request_to_dict(app_request_instance: AppRequest) -> dict:
    return {
        'app_name': app_request_instance.app_name,
        'id': app_request_instance.id,
        'app_id': app_request_instance.app_id,
        'app': convert_app_to_dict(app_request_instance.app) if app_request_instance.app else None
    }
