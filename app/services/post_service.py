import logging
from typing import Type

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.models.post import Post
from app.repositories import post_repository
from app.schemas.post import PostCreate

logger = logging.getLogger(__name__)


def create_post(db: Session, request_body: PostCreate) -> dict:
    try:
        post_obj = Post(**request_body.model_dump())
        post_obj = post_repository.create_post(db, post_obj)
        logger.info(f"Post created successfully with post_id: {post_obj.id}")
        return {"detail": "Post created successfully"}
    except Exception as ex:
        logger.error(f"Error while creating post: {ex}")
        db.rollback()
        raise


def get_post(post_id: int, db: Session) -> Type[Post]:
    logger.info(f"Retrieving post with post_id: {post_id}")
    post = post_repository.get_post_by_id(db, post_id)
    if post is None:
        logger.warning(f"Post with post_id {post_id} not found")
        raise NotFoundException(post_id)
    return post


def get_all_posts(db: Session) -> list[Type[Post]]:
    logger.info("Retrieving all posts from the database")
    return post_repository.get_all_post(db)
