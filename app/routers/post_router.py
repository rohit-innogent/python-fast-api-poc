from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.custom_exceptions.custom_exceptions import NotFoundException
from app.schemas.post import PostResponse, PostCreate
from app.security.auth import get_current_user

from app.services import post_service
import logging
router = APIRouter()


logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create_post", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        return post_service.create_post(db, post)
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating post")


@router.get("/get_by_id/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post_by_id(user: user_dependency, post_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"user validated successfully: {user}")
        return post_service.get_post(post_id, db)
    except NotFoundException as ex:
        raise ex
    except Exception as ex:
        logger.error(f"Exception while fetching post by Id: {post_id}, exception: {ex}")
        raise HTTPException(status_code=500, detail="Error retrieving post")


@router.get("/get_all", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(user: user_dependency, db: Session = Depends(get_db)):
    try:
        logger.info(f"user validated successfully: {user}")
        posts = post_service.get_all_posts(db)
        return posts
    except Exception as ex:
        logger.error(f"Error fetching posts: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching posts")
