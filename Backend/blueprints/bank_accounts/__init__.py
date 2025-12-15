from flask import Blueprint

bank_accounts_bp = Blueprint(
    "bank_accounts", 
    __name__,
    url_prefix="/bank_accounts/"
)

from . import routes