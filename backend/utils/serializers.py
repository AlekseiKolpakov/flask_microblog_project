from ..models.tweet import Tweet
from ..models.user import User


def serialize_user_short(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
    }


def serialize_user_profile(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "followers": [serialize_user_short(f.follower) for f in user.followers],
        "following": [serialize_user_short(f.followed) for f in user.following],
    }


def serialize_tweets(tweets):
    return [serialize_tweet(tweet) for tweet in tweets]


def serialize_tweet(tweet: Tweet):
    return {
        "id": tweet.id,
        "content": tweet.text or "",
        "attachments": [m.url for m in tweet.medias],
        "author": {
            "id": tweet.author.id,
            "name": tweet.author.name,
        },
        "likes": [
            {
                "user_id": like.user.id,
                "name": like.user.name,
            }
            for like in tweet.likes
        ],
    }
