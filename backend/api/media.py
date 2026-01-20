from flask import g, request
from flask_restx import Namespace, Resource

from ..core.auth import auth_required
from ..core.db import SessionLocal
from ..services.media import save_media
from ..utils.responses import error, success

api = Namespace("media", description="Media")


@api.route("")
class Media(Resource):

    @auth_required
    def post(self):
        file = request.files.get("file")
        if not file:
            return error("validation_error", "file is required", 400)

        with SessionLocal() as db:
            media = save_media(db, file, g.user.id)

        return success({"media_id": media.id})
