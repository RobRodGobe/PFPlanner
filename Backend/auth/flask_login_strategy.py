from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user, login_required
from .base import AuthStrategy


class FlaskLoginStrategy(AuthStrategy):
    def protect_route(self, func, required_role=None):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if required_role and (not current_user.is_authenticated or current_user.role != required_role):
                abort(403)
            return func(*args, **kwargs)
        return wrapper

    def get_current_user(self, request):
        return current_user if current_user.is_authenticated else None
