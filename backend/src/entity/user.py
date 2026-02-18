from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, func, String
from datetime import datetime
from typing import TYPE_CHECKING, List

from src.entity.base import Base
if TYPE_CHECKING:
    from src.entity.user_search_log import UserSearchLog

class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    logs: Mapped[List["UserSearchLog"]] = relationship(
        "UserSearchLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )