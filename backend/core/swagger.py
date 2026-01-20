from flask_restx import Api, fields
from werkzeug.exceptions import HTTPException

from ..utils.responses import error

ERROR_TYPE_BY_STATUS = {
    401: "auth_error",
    403: "permission_error",
    404: "not_found",
    422: "validation_error",
}


class CustomApi(Api):
    def handle_error(self, e):
        # HTTP ошибки (401, 403, 404, ...)
        if isinstance(e, HTTPException):
            return error(
                error_type=ERROR_TYPE_BY_STATUS.get(e.code, "http_error"),
                message=e.description or "Error",
                status=e.code or 500,
            )

        # Неожиданные ошибки
        return error(
            error_type="internal_error",
            message="Internal server error",
            status=500,
        )


api = CustomApi(
    title="Microblog API",
    version="1.0",
    description="Microblog backend",
    doc="/docs",
    authorizations={
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "api-key",
        }
    },
    security="apiKey",
)


user_short = api.model(
    "UserShort",
    {
        "id": fields.Integer,
        "name": fields.String,
    },
)

user_profile = api.model(
    "UserProfile",
    {
        "id": fields.Integer,
        "name": fields.String,
        "followers": fields.List(fields.Nested(user_short)),
        "following": fields.List(fields.Nested(user_short)),
    },
)

author_model = api.model(
    "Author",
    {
        "id": fields.Integer,
        "name": fields.String,
    },
)


def get_tweet_create_model(api):
    return api.model(
        "TweetCreate",
        {
            "tweet_data": fields.String(required=True),
            "tweet_media_ids": fields.List(fields.Integer, required=False),
        },
    )


like_user_model = api.model(
    "LikeUser",
    {
        "user_id": fields.Integer,
        "name": fields.String,
    },
)

tweet_model = api.model(
    "Tweet",
    {
        "id": fields.Integer,
        "content": fields.String,
        "attachments": fields.List(fields.String),
        "author": fields.Nested(author_model),
        "likes": fields.List(fields.Nested(like_user_model)),
    },
)

tweets_response = api.model(
    "TweetsResponse",
    {
        "result": fields.Boolean,
        "tweets": fields.List(fields.Nested(tweet_model)),
    },
)

tweet_created_response = api.model(
    "TweetCreatedResponse",
    {
        "result": fields.Boolean,
        "tweet_id": fields.Integer,
    },
)

tweet_deleted_response = api.model(
    "TweetDeletedResponse",
    {
        "result": fields.Boolean,
    },
)

simple_response = api.model(
    "SimpleResponse",
    {
        "result": fields.Boolean,
    },
)

user_profile_response = api.model(
    "UserProfileResponse",
    {
        "result": fields.Boolean,
        "user": fields.Nested(user_profile),
    },
)
