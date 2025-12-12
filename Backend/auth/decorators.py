from functools import wraps
from flask import current_app

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        strategy = current_app.auth_strategy
        protected = strategy.protect_route(func)
        return protected(*args, **kwargs)
    return wrapper
