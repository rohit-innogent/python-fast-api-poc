from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base import Base
# from app.model import Adhar

from app.model.post import Post

if TYPE_CHECKING:
    from app.model.role import Role
    from app.model.adhar import Adhar

# Associate table for many-to-many relationship between user an post
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id")),
)

# User is having one-to-one mapping with Adhar, one-to-many with Post and many-to-many with Role
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    # posts: Mapped[List["Post"]] = relationship('Post', back_populates="user")
    posts: Mapped[List["Post"]] = relationship()
    roles: Mapped[List["Role"]] = relationship('Role', secondary=user_role, back_populates="users")
    # adhar: Mapped["Adhar"] = relationship(back_populates="users")
    adhar: Mapped["Adhar"] = relationship(back_populates="user")


def __repr__(self):
    return f'<User: {self.username}>'

# Many-to-many relationship
# Associate table for many-to-many relationship between user an post
# user_post = Table(
#     "user_post",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id")),
#     Column("post_id", ForeignKey("posts.id")),
# )
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     username: Mapped[str] = mapped_column(String(50))
#     post: Mapped[List["Post"]] = relationship(secondary=user_post)
#
#     # __init__()
#     def __repr__(self):
#         return f'<User: {self.username} posts: {self.post}>'
#
#
# class Post(Base):
#     __tablename__ = 'posts'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     title: Mapped[str] = mapped_column(String(50))
#     # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped[List["User"]] = relationship(secondary=user_post)
#
#     def __repr__(self):
#         return f'<Post: {self.title}>'


#  One-to-one relationship
#     class User(Base):
#         __tablename__ = 'users'
#
#         id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#         username: Mapped[str] = mapped_column(String(50), unique=True)
#         post: Mapped["Post"] = relationship(back_populates="user")
#
#     class Post(Base):
#         __tablename__ = 'posts'
#
#         id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#         title: Mapped[str] = mapped_column(String(50))
#         user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#         user: Mapped["User"] = relationship(back_populates="post")


# Many-to-one relationship
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     username: Mapped[str] = mapped_column(String(50), unique=True)
#     post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
#     post: Mapped["Post"] = relationship()
#
#
# class Post(Base):
#     __tablename__ = 'posts'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     title: Mapped[str] = mapped_column(String(50))
