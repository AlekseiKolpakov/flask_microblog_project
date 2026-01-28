from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base

if TYPE_CHECKING:
    from ..models.tweet import Tweet
    from ..models.user import User


class Media(Base):
    """
    Модель загруженного медиа-файла (изображения).

    Медиа может быть:
    - загружено пользователем
    - позже прикреплено к твиту
    """

    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)

    # URL до файла
    url: Mapped[str] = mapped_column(String, nullable=False)

    # Владелец файла
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Твит, к которому прикреплён файл (опционально)
    tweet_id: Mapped[int | None] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Связи
    tweet: Mapped["Tweet"] = relationship(back_populates="medias")
    owner: Mapped["User"] = relationship(back_populates="uploaded_medias")
