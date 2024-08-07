from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.base import Base
from app.models import App


# AppRequest is having many-to-one mapping with App
class AppRequest(Base):
    __tablename__ = "app_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    app_name: Mapped[str] = mapped_column(String(50), unique=True)
    app_id: Mapped[int] = mapped_column(Integer, ForeignKey("apps.id"))
    app: Mapped['App'] = relationship()
