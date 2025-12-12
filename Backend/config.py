import os

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Auth flags
    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    AUTH_STRATEGY = os.getenv("AUTH_STRATEGY", "noauth")

    # Feature flags
    FEATURE_CALCULATORS = os.getenv("FEATURE_CALCULATORS", "true").lower() == "true"
    FEATURE_ACCOUNTS = os.getenv("FEATURE_ACCOUNTS", "true").lower() == "true"
    FEATURE_BUDGET = os.getenv("FEATURE_BUDGET", "true").lower() == "true"
    FEATURE_RETIREMENT = os.getenv("FEATURE_RETIREMENT", "true").lower() == "true"
    FEATURE_EDUCATION = os.getenv("FEATURE_EDUCATION", "true").lower() == "true"

    # Dark mode toggle
    FEATURE_DARK_MODE = os.getenv("FEATURE_DARK_MODE", "true").lower() == "true"

    # Maintenance mode
    FEATURE_MAINTENANCE = os.getenv("FEATURE_MAINTENANCE", "false").lower() == "true"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    PREFERRED_URL_SCHEME = "https"
    SERVER_NAME = os.getenv("CODESPACE_NAME") + "-5000.app.github.dev"

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    AUTH_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
