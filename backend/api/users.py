from flask import g
from flask_restx import Namespace, Resource

from ..core.auth import auth_required
from ..core.db import SessionLocal
from ..core.swagger import simple_response, user_profile, user_profile_response
from ..services.follows import follow_user, unfollow_user
from ..services.users import get_user_by_id
from ..utils.responses import error, success
from ..utils.serializers import serialize_user_profile

api = Namespace("users", description="Users")


@api.route("/me")
class Me(Resource):

    @auth_required
    @api.marshal_with(user_profile_response, code=200)
    def get(self):
        return success(
            {
                "user": serialize_user_profile(g.user),
            }
        )


@api.route("/<int:user_id>")
class User(Resource):

    @auth_required
    @api.marshal_with(user_profile, code=200)
    def get(self, user_id: int):
        with SessionLocal() as db:
            user = get_user_by_id(db, user_id)
            if not user:
                return error("not_found", "User not found", 404)

        return success(
            {
                "user": serialize_user_profile(user),
            }
        )


@api.route("/<int:user_id>/follow")
class Follow(Resource):

    @auth_required
    @api.marshal_with(simple_response, code=200)
    def post(self, user_id: int):
        with SessionLocal() as db:
            follow_user(db, g.user.id, user_id)
        return success()

    @auth_required
    @api.marshal_with(simple_response, code=200)
    def delete(self, user_id: int):
        with SessionLocal() as db:
            unfollow_user(db, g.user.id, user_id)
        return success()
