from sqlalchemy.orm import Session

from ..models.follow import Follow


def follow_user(
    db: Session,
    current_user_id: int,
    target_user_id: int,
) -> bool:
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
