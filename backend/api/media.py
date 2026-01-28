from flask import g, request
from flask_restx import Namespace, Resource

from ..core.auth import auth_required
from ..core.db import SessionLocal
from ..services.media import save_media
from ..utils.responses import error, success

# Namespace для загрузки медиафайлов
api = Namespace("media", description="Media")


@api.route("")
class Media(Resource):
    """
    Работа с медиафайлами (загрузка изображений/файлов).
    """

    @auth_required
    def post(self):
        """
        Загрузить медиафайл.

        Ожидает multipart/form-data с файлом в поле "file".

        :return: JSON c идентификатором загруженного файла
        {
            "result": true,
            "media_id": int
        }
        """
        file = request.files.get("file")
        if not file:
            return error("validation_error", "file is required", 400)

        with SessionLocal() as db:
            media = save_media(db, file, g.user.id)

        return success({"media_id": media.id})
