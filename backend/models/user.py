from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base

if TYPE_CHECKING:
    from ..models.follow import Follow
    from ..models.like import Like
    from ..models.media import Media
    from ..models.tweet import Tweet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    tweets: Mapped[List["Tweet"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    likes: Mapped[List["Like"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    followers: Mapped[List["Follow"]] = relationship(
        foreign_keys="Follow.followed_id",
        back_populates="followed",
    )

    following: Mapped[List["Follow"]] = relationship(
        foreign_keys="Follow.follower_id",
        back_populates="follower",
    )

    uploaded_medias: Mapped[List["Media"]] = relationship(
        back_populates="owner",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name}>"
