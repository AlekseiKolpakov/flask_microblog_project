from sqlalchemy.orm import Session, selectinload

from ..models.follow import Follow
from ..models.user import User


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .options(
            selectinload(User.followers).selectinload(Follow.follower),
            selectinload(User.following).selectinload(Follow.followed),
        )
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_api_key(db, api_key: str):
    return (
        db.query(User)
        .options(
            selectinload(User.followers).selectinload(Follow.follower),
            selectinload(User.following).selectinload(Follow.followed),
        )
        .filter(User.api_key == api_key)
        .first()
    )
