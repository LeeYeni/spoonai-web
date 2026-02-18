from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING

from src.entity.base import Base
if TYPE_CHECKING:
    from src.entity.user import User

class UserSearchLog(Base):
    __tablename__ = "user_search_log_table"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user_table.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    query: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="logs"
    )