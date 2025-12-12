from functools import wraps
from flask import g
from .base import AuthStrategy

class NoAuthStrategy(AuthStrategy):
    def protect_route(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            g.current_user = None
            return func(*args, **kwargs)
        return wrapper

    def get_current_user(self, request):
        return None
