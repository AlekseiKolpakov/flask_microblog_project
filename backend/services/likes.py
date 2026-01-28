from sqlalchemy.orm import Session

from ..models.like import Like


def like_tweet(db: Session, user_id: int, tweet_id: int) -> bool:
    """
    Поставить лайк на твит.

    Если лайк уже существует — ничего не делает.

    :param db: SQLAlchemy сессия
    :param user_id: ID пользователя
    :param tweet_id: ID твита
    :return: True — операция выполнена успешно
    """
    exists = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.tweet_id == tweet_id,
        )
        .first()
    )

    if exists:
        return True

    like = Like(user_id=user_id, tweet_id=tweet_id)
    db.add(like)
    db.commit()
    return True


def unlike_tweet(db: Session, user_id: int, tweet_id: int) -> bool:
    """
    Убрать лайк с твита.

    Если лайка нет — ничего не делает.

    :param db: SQLAlchemy сессия
    :param user_id: ID пользователя
    :param tweet_id: ID твита
    :return: True — операция выполнена успешно
    """
    like = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.tweet_id == tweet_id,
        )
        .first()
    )

    if like:
        db.delete(like)
        db.commit()

    return True
