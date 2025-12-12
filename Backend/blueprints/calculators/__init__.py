from flask import Blueprint

calculators_bp = Blueprint(
    "calculators", 
    __name__,
    url_prefix="/calculators"
)

from . import routes