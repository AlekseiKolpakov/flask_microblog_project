from flask import g
from flask_restx import Namespace, Resource

from ..core.auth import auth_required
from ..core.db import SessionLocal
from ..core.swagger import simple_response
from ..services.likes import like_tweet, unlike_tweet
from ..utils.responses import success

api = Namespace("tweets", description="Tweet likes")


@api.route("/<int:tweet_id>/likes")
class TweetLikes(Resource):

    @auth_required
    @api.marshal_with(simple_response, code=200)
    def post(self, tweet_id: int):
        with SessionLocal() as db:
            like_tweet(db, g.user.id, tweet_id)
        return success()

    @auth_required
    @api.marshal_with(simple_response, code=200)
    def delete(self, tweet_id: int):
        with SessionLocal() as db:
            unlike_tweet(db, g.user.id, tweet_id)
        return success()
