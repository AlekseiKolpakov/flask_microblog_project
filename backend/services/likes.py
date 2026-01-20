from sqlalchemy.orm import Session

from ..models.like import Like


def like_tweet(db: Session, user_id: int, tweet_id: int) -> bool:
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
