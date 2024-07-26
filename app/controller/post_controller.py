from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schema.post import PostResponse, PostCreate

from app.service import post_service
import logging
router = APIRouter()


logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        post_service.create_post(db, post)
        return "Post created successfully"
    except Exception as ex:
        logger.error(f"Error creating post with title {post.title}: {ex}")
        raise HTTPException(status_code=500, detail="Error creating post")


@router.get("/get_by_id/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    try:
        post = post_service.get_post(post_id, db)
        if post is None:
            logger.error(f"Post with ID {post_id} not found")
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as ex:
        logger.error(f"Error retrieving post with ID {post_id}: {ex}")
        raise HTTPException(status_code=500, detail="Error retrieving post")


@router.get("/get_all", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(db: Session = Depends(get_db)):
    try:
        posts = post_service.get_all_posts(db)
        return posts
    except Exception as ex:
        logger.error(f"Error fetching posts: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching posts")
