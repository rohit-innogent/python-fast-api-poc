import logging

from sqlalchemy.orm import Session

from app.model.post import Post
from app.schema.post import PostCreate

logger = logging.getLogger(__name__)


def create_post(db: Session, post: PostCreate):
    try:
        post_obj = Post(**post.model_dump())
        db.add(post_obj)
        db.commit()
        db.refresh(post_obj)
        logger.info(f"Post created successfully with post_id: {post_obj.id}")
    except Exception as ex:
        logger.error(f"Error creating post: {ex}")
        db.rollback()
        raise


def get_all_posts(db: Session):
    try:
        logger.info("Retrieving all posts from the database")
        return db.query(Post).all()
    except Exception as ex:
        logger.error(f"Error retrieving all posts: {ex}")
        raise


def get_post(post_id: int, db: Session):
    try:
        logger.info(f"Retrieving post with post_id: {post_id}")
        post = db.query(Post).filter(Post.id == post_id).first()
        if post is None:
            logger.warning(f"Post with post_id {post_id} not found")
        return post
    except Exception as ex:
        logger.error(f"Error retrieving post with post_id {post_id}: {ex}")
        raise
