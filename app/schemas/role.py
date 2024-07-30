from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

from app.schemas.user import UserBase


class UserResponse(UserBase):
    id: int


class RoleBase(BaseModel):
    role_name: str
    role_desc: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int
    users: Optional[List['UserResponse']] = None

    class Config:
        from_attributes = True


class RoleResponseForUser(RoleBase):
    id: int

    class Config:
        from_attributes = True
