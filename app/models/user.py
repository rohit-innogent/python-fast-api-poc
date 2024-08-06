from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base import Base

from app.models.post import Post

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.aadhar import Adhar

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
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    posts: Mapped[List["Post"]] = relationship()
    roles: Mapped[List["Role"]] = relationship('Role', secondary=user_role, back_populates="users")
    adhar: Mapped["Adhar"] = relationship(back_populates="user")


def __repr__(self):
    return f'<User: {self.username}>'
