from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schema.post import PostResponse, PostResponseForUser


class UserBase(BaseModel):
    username: Optional[str]
    email: EmailStr
    age: Optional[int] = None
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    roles: List[str] = ["User Role"]
    password: str


class AdharResponseForUser(BaseModel):
    adhar_id: str
    id: int


class RoleResponseForUser(BaseModel):
    role_name: str
    role_desc: str
    id: int


class UserResponse(UserBase):
    id: int
    roles: Optional[List['RoleResponseForUser']] = None
    posts: Optional[List['PostResponseForUser']] = None
    adhar: Optional['AdharResponseForUser'] = None

    class Config:
        from_attributes = True


class UserResponseForAdhar(UserBase):
    id: int

    class Config:
        from_attributes = True
