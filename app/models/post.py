from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.config.base import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    # category: Mapped["Category"] = relationship()
    # user: Mapped["User"] = relationship('User', back_populates="posts")
