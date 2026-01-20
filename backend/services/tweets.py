from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import Session, selectinload

from ..models.follow import Follow
from ..models.like import Like
from ..models.media import Media
from ..models.tweet import Tweet


def create_tweet(
    db: Session,
    author_id: int,
    text: str,
    media_ids: list[int] | None = None,
) -> Tweet:
    tweet = Tweet(
        author_id=author_id,
        text=text,
    )
    db.add(tweet)
    db.flush()

    if media_ids:
        medias = (
            db.query(Media)
            .filter(
                Media.id.in_(media_ids),
                Media.owner_id == author_id,
            )
            .all()
        )
        for media in medias:
            media.tweet_id = tweet.id

    db.commit()
    db.refresh(tweet)
    return tweet


def delete_tweet(db: Session, tweet: Tweet) -> bool:
    db.delete(tweet)
    db.commit()
    return True


def get_feed_for_user(
    db,
    user_id: int,
    limit: int = 20,
    offset: int = 0,
):
    return (
        db.query(Tweet)
        .outerjoin(Like)  # outerjoin, чтобы твиты без лайков не пропали
        .filter(
            or_(
                Tweet.author_id == user_id,
                Tweet.author_id.in_(
                    select(Follow.followed_id).where(Follow.follower_id == user_id)
                ),
            )
        )
        .options(
            selectinload(Tweet.author),
            selectinload(Tweet.medias),
            selectinload(Tweet.likes).selectinload(Like.user),
        )
        .group_by(Tweet.id)  # обязательно для COUNT
        .order_by(
            desc(func.count(Like.id)),  # сортировка по популярности
            desc(Tweet.created_at),  # вторичная сортировка
        )
        .limit(limit)
        .offset(offset)
        .all()
    )
