from flask import g, request
from flask_restx import Namespace, Resource

from ..core.auth import auth_required
from ..core.db import SessionLocal
from ..core.swagger import (
    get_tweet_create_model,
    tweet_created_response,
    tweet_deleted_response,
    tweets_response,
)
from ..models.tweet import Tweet
from ..services.tweets import create_tweet, get_feed_for_user
from ..utils.responses import error, success
from ..utils.serializers import serialize_tweets

# Namespace для работы с твитами
api = Namespace("tweets", description="Tweets")

# Модель запроса для создания твита
tweet_create_model = get_tweet_create_model(api)


@api.route("")
class Tweets(Resource):
    """
    Работа со списком твитов:
    - получение ленты
    - создание нового твита
    """

    @auth_required
    @api.marshal_with(tweets_response, code=200)
    def get(self):
        """
        Получить ленту твитов текущего пользователя.

        Поддерживает параметры:
        - limit (по умолчанию 20, максимум 100)
        - offset (по умолчанию 0)

        :return: JSON со списком твитов
        """
        limit = min(int(request.args.get("limit", 20)), 100)
        offset = int(request.args.get("offset", 0))

        with SessionLocal() as db:
            tweets = get_feed_for_user(
                db=db,
                user_id=g.user.id,
                limit=limit,
                offset=offset,
            )

        return success(
            {
                "tweets": serialize_tweets(tweets),
            }
        )

    @api.expect(tweet_create_model, validate=True)
    @auth_required
    @api.marshal_with(tweet_created_response, code=200)
    def post(self):
        """
        Создать новый твит.

        Ожидает JSON:
        {
            "tweet_data": str,
            "tweet_media_ids": [int]
        }
        :return: JSON с ID созданного твита
        """
        data = request.json
        if not data or "tweet_data" not in data:
            return error("validation_error", "tweet_data is required", 400)

        with SessionLocal() as db:
            tweet = create_tweet(
                db=db,
                author_id=g.user.id,
                text=data["tweet_data"],
                media_ids=data.get("tweet_media_ids", []),
            )

        return success({"tweet_id": tweet.id}, 200)


@api.route("/<int:tweet_id>")
class TweetItem(Resource):
    """
    Работа с конкретным твитом.
    """

    @auth_required
    @api.marshal_with(tweet_deleted_response, code=200)
    def delete(self, tweet_id: int):
        """
        Удалить твит текущего пользователя.

        :param tweet_id: ID твита
        :return: JSON с результатом операции
        """
        with SessionLocal() as db:
            tweet = (
                db.query(Tweet)
                .filter(
                    Tweet.id == tweet_id,
                    Tweet.author_id == g.user.id,
                )
                .first()
            )

            if not tweet:
                return error("not_found", "Tweet not found", 404)

            db.delete(tweet)
            db.commit()

        return success()
