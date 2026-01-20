from functools import wraps

from flask import g, request
from flask_restx import abort

from ..core.db import SessionLocal
from ..services.users import get_user_by_api_key


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("api-key")
        if not api_key:
            abort(401, "api-key header is required")

        with SessionLocal() as db:
            user = get_user_by_api_key(db, api_key)
            if not user:
                abort(401, "Invalid api-key")

            g.user = user

        return fn(*args, **kwargs)

    return wrapper
