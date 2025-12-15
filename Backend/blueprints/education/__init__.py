from flask import Blueprint

education_bp = Blueprint(
    "education", 
    __name__,
    url_prefix="/education/"
)

from . import routes