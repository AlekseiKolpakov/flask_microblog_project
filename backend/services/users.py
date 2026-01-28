from sqlalchemy.orm import Session, selectinload

from ..models.follow import Follow
from ..models.user import User


def get_user_by_id(db: Session, user_id: int):
    """
    Получить пользователя по ID с подгрузкой подписок.

    :param db: SQLAlchemy сессия
    :param user_id: ID пользователя
    :return: Объект User или None
    """
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
    """
    Получить пользователя по API-ключу.

    Используется для аутентификации.

    :param db: SQLAlchemy сессия
    :param api_key: API-ключ пользователя
    :return: Объект User или None
    """
    return (
        db.query(User)
        .options(
            selectinload(User.followers).selectinload(Follow.follower),
            selectinload(User.following).selectinload(Follow.followed),
        )
        .filter(User.api_key == api_key)
        .first()
    )
