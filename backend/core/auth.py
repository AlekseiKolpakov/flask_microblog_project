from functools import wraps

from flask import g, request
from flask_restx import abort

from ..core.db import SessionLocal
from ..services.users import get_user_by_api_key


def auth_required(fn):
    """
    Декоратор для защиты эндпоинтов.

    Проверяет наличие API-ключа в заголовке запроса (`api-key`),
    находит пользователя в базе данных и сохраняет его в `flask.g`.

    В случае ошибки:
    - 401, если заголовок отсутствует
    - 401, если API-ключ некорректный

    :param fn: Оборачиваемая функция (endpoint)
    :return: Обёрнутая функция с проверкой авторизации
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Получаем API-ключ из заголовков
        api_key = request.headers.get("api-key")
        if not api_key:
            abort(401, "api-key header is required")

        # Ищем пользователя по API-ключу
        with SessionLocal() as db:
            user = get_user_by_api_key(db, api_key)
            if not user:
                abort(401, "Invalid api-key")

            # Сохраняем пользователя в контекст запросов
            g.user = user

        return fn(*args, **kwargs)

    return wrapper
