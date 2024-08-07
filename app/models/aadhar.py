from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base import Base

from app.models.user import User


class Adhar(Base):
    __tablename__ = "adhars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    adhar_id: Mapped[str] = mapped_column(String(12), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="adhar")

    # id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # adhar_id: Mapped[str] = mapped_column(String(12), unique=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship(back_populates="adhar")
