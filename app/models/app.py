from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.base import Base


class App(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    app_name: Mapped[str] = mapped_column(String(50), unique=True)
    app_desc: Mapped[str] = mapped_column(String(100))
