from sqlalchemy.orm import Session

from ..models.follow import Follow


def follow_user(
    db: Session,
    current_user_id: int,
    target_user_id: int,
) -> bool:
    """
    Подписать текущего пользователя на другого пользователя.

    Если подписка уже существует — ничего не делает.

    :param db: SQLAlchemy сессия
    :param current_user_id: ID пользователя, который подписывается
    :param target_user_id: ID пользователя, на которого подписываются
    :return: True — операция выполнена успешно
    """
    # Проверяем, существует ли уже подписка
    exists = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user_id,
            Follow.followed_id == target_user_id,
        )
        .first()
    )

    if exists:
        return True

    # Создаём новую подписку
    follow = Follow(
        follower_id=current_user_id,
        followed_id=target_user_id,
    )

    db.add(follow)
    db.commit()
    return True


def unfollow_user(
    db: Session,
    current_user_id: int,
    target_user_id: int,
) -> bool:
    """
    Отписать текущего пользователя от другого пользователя.

    Если подписки нет — ничего не делает.

    :param db: SQLAlchemy сессия
    :param current_user_id: ID пользователя, который отписывается
    :param target_user_id: ID пользователя, от которого отписываются
    :return: True — операция выполнена успешно
    """
    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user_id,
            Follow.followed_id == target_user_id,
        )
        .first()
    )

    if follow:
        db.delete(follow)
        db.commit()

    return True
