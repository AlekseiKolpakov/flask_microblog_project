import os

from flask import Flask, send_from_directory

# Глобальный экземпляр Swagger API с кастомным error handler
from .core.swagger import api

# Базовая директория проекта
BASE_DIR = os.getcwd()

# Директория для загруженных файлов (media)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def create_app() -> Flask:
    """
    Application factory.
    Создаёт и конфигурирует Flask-приложение.
    Используется для корректной инициализации app, Swagger и namespaces.
    """
    app = Flask(__name__)

    # Endpoint для раздачи загруженных файлов (картинок)
    # Пример: /uploads/image_123.png
    @app.route("/uploads/<path:filename>")
    def uploads(filename: str):
        return send_from_directory(UPLOAD_DIR, filename)

    # Импорт API namespaces
    # Каждый namespace отвечает за свою предметную область
    from .api.likes import api as likes_ns
    from .api.media import api as media_ns
    from .api.tweets import api as tweets_ns
    from .api.users import api as users_ns

    # Инициализация Swagger (Flask-RESTX) на приложении
    api.init_app(app)

    # Регистрация namespaces и их URL-префиксов
    api.add_namespace(tweets_ns, path="/api/tweets")
    api.add_namespace(users_ns, path="/api/users")
    api.add_namespace(media_ns, path="/api/medias")

    # likes относятся к твитам, поэтому живут под /api/tweets/<id>/likes
    api.add_namespace(likes_ns, path="/api/tweets")

    return app


# Экземпляр приложения (используется gunicorn / flask run)
app = create_app()
