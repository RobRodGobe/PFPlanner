from Backend.auth.noauth_strategy import NoAuthStrategy
from Backend.auth.flask_login_strategy import FlaskLoginStrategy
from Backend.auth.jwt_strategy import JWTStrategy
from Backend.auth import get_auth_strategy


def test_auth_strategy_noauth_by_default(app):
    app.config["AUTH_ENABLED"] = False
    strategy = get_auth_strategy(app)
    assert isinstance(strategy, NoAuthStrategy)


def test_auth_strategy_flask_login(app):
    app.config["AUTH_ENABLED"] = True
    app.config["AUTH_STRATEGY"] = "flask_login"
    strategy = get_auth_strategy(app)
    assert isinstance(strategy, FlaskLoginStrategy)


def test_auth_strategy_jwt(app):
    app.config["AUTH_ENABLED"] = True
    app.config["AUTH_STRATEGY"] = "jwt"
    strategy = get_auth_strategy(app)
    assert isinstance(strategy, JWTStrategy)
