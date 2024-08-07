from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base import Base
from app.models.user import User, user_role


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True)
    role_desc: Mapped[str] = mapped_column(String(100))
    users: Mapped[List["User"]] = relationship('User', secondary=user_role, back_populates="roles")

