from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)

from flask import request

@pages_bp.get("/debug-env")
def debug_env():
    return {
        "host": request.host,
        "url": request.url,
        "base_url": request.base_url,
        "headers": dict(request.headers),
        "environ": {
            "HTTP_HOST": request.environ.get("HTTP_HOST"),
            "SERVER_NAME": request.environ.get("SERVER_NAME"),
            "SERVER_PORT": request.environ.get("SERVER_PORT"),
            "HTTP_X_FORWARDED_HOST": request.environ.get("HTTP_X_FORWARDED_HOST"),
            "HTTP_X_FORWARDED_PORT": request.environ.get("HTTP_X_FORWARDED_PORT"),
            "HTTP_X_FORWARDED_PROTO": request.environ.get("HTTP_X_FORWARDED_PROTO"),
        }
    }
