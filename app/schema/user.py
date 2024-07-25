from typing import Annotated, Optional, List

from fastapi import Query
from pydantic import BaseModel, EmailStr

from app.model.post import Post
from app.schema.post import PostResponse


class UserBase(BaseModel):
    username: Optional[str]
    email: EmailStr
    age: Optional[int] = None
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    posts: Optional[List['PostResponse']] = None

    class Config:
        from_attributes = True

