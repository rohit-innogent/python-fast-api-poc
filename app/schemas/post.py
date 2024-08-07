from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None


class PostCreate(PostBase):
    user_id: int


class PostResponse(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class PostResponseForUser(PostBase):
    id: int

    class Config:
        from_attributes = True
