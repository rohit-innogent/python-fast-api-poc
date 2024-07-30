from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel

from app.schemas.user import UserResponseForAdhar


class AdharBase(BaseModel):
    adhar_id: str
    user_id: int


class AdharCreate(AdharBase):
    pass


class AdharResponse(AdharBase):
    id: int
    user: Optional['UserResponseForAdhar'] = None

    class Config:
        from_attributes = True
