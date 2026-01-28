from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base

if TYPE_CHECKING:
    from ..models.user import User


class Follow(Base):
    """
    Модель подписки одного пользователя на другого.

    Используется для реализации функционала follow / unfollow
    и построения ленты твитов.
    """

    __tablename__ = "follows"

    # Запрещает дубли подписок (один и тот же пользователь
    # не может подписаться на другого более одного раза)
    __table_args__ = (UniqueConstraint("follower_id", "followed_id", name="uq_follow_pair"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    # Кто подписался
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # На кого подписались
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Дата создание подписки
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Связи с пользователями
    follower: Mapped["User"] = relationship(
        foreign_keys=[follower_id],
        back_populates="following",
    )

    followed: Mapped["User"] = relationship(
        foreign_keys=[followed_id],
        back_populates="followers",
    )
