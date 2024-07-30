from typing import Type

from sqlalchemy.orm import Session

from app.models import Post


def create_post(db: Session, post_obj: Post) -> Post:
    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)
    return post_obj


def get_post_by_id(db: Session, post_id: int) -> Type[Post] | None:
    return db.query(Post).filter(Post.id == post_id).first()


def get_all_post(db: Session) -> list[Type[Post]]:
    return db.query(Post).all()
