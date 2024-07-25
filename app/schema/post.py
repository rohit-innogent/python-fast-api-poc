from typing import List, Optional

from pydantic import BaseModel

from app.model.post import Post


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
