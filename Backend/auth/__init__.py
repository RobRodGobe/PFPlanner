from flask import current_app
from .noauth_strategy import NoAuthStrategy
from .flask_login_strategy import FlaskLoginStrategy
from .jwt_strategy import JWTStrategy

def get_auth_strategy(app):
    if not app.config.get("AUTH_ENABLED", False):
        return NoAuthStrategy()

    strategy_name = app.config.get("AUTH_STRATEGY", "noauth").lower()
    if strategy_name == "flask_login":
        return FlaskLoginStrategy()
    elif strategy_name == "jwt":
        return JWTStrategy()
    else:
        return NoAuthStrategy()
