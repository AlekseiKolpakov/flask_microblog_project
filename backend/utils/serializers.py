from ..models.tweet import Tweet
from ..models.user import User


def serialize_user_short(user: User) -> dict:
    """
    Краткая сериализация пользователя.

    Используется в списках подписчиков, лайков и т.п.

    :param user: Объект User
    :return: Словарь с краткой информацией о пользователе
    """
    return {
        "id": user.id,
        "name": user.name,
    }


def serialize_user_profile(user: User) -> dict:
    """
    Полная сериализация профиля пользователя.

    Используется в эндпоинтах:
    - GET /api/users/me
    - GET /api/users/<id>

    :param user: Объект User
    :return: Словарь с профилем пользователя
    """
    return {
        "id": user.id,
        "name": user.name,
        "followers": [serialize_user_short(f.follower) for f in user.followers],
        "following": [serialize_user_short(f.followed) for f in user.following],
    }


def serialize_tweets(tweets):
    """
    Сериализация списка твитов.

    :param tweets: Список объектов Tweet
    :return: Список сериализованных твитов
    """
    return [serialize_tweet(tweet) for tweet in tweets]


def serialize_tweet(tweet: Tweet):
    """
    Сериализация одного твита.

    Формат соответствует требованиям ТЗ и Swagger-документации.

    :param tweet: Объект Tweet
    :return: Словарь с данными твита
    """
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
