from functools import wraps
from flask import current_app, abort

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            strategy = current_app.auth_strategy
            # Protect route with base auth first
            protected = strategy.protect_route(func)
            # After basic auth, enforce role
            result = protected(*args, **kwargs)

            user = strategy.get_current_user(request=None)
            if not user or user.role != role:
                abort(403)
            return result
        return wrapper
    return decorator
