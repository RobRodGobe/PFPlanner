from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from .base import AuthStrategy

class JWTStrategy(AuthStrategy):
    def protect_route(self, func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def get_current_user(self, request):
        return get_jwt_identity()
