from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base

if TYPE_CHECKING:
    from ..models.tweet import Tweet
    from ..models.user import User


class Like(Base):
    """
    Модель лайка твита пользователем.

    Один пользователь может поставить лайк
    одному твиту только один раз.
    """

    __tablename__ = "likes"

    # Запрет дублирования лайков
    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="uq_user_tweet_like"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Связи
    user: Mapped["User"] = relationship(back_populates="likes")
    tweet: Mapped["Tweet"] = relationship(back_populates="likes")
