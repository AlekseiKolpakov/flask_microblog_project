from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base

if TYPE_CHECKING:
    from ..models.like import Like
    from ..models.media import Media
    from ..models.user import User


class Tweet(Base):
    """
    Модель твита.

    Основная сущность сервиса микроблогов.
    """

    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Текст твита
    text: Mapped[str] = mapped_column(String, nullable=False)

    # Автор твита
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    # Связи
    author: Mapped["User"] = relationship(back_populates="tweets")

    medias: Mapped[list["Media"]] = relationship(
        back_populates="tweet",
        cascade="all, delete-orphan",
    )

    likes: Mapped[list["Like"]] = relationship(
        back_populates="tweet",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Tweet id={self.id} author_id={self.author_id}>"
