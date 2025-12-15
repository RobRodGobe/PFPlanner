from flask import Blueprint

retirement_bp = Blueprint(
    "retirement", 
    __name__,
    url_prefix="/retirement/"
)


from . import routes