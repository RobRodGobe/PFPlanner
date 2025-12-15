from flask import render_template
from . import bank_accounts_bp

@bank_accounts_bp.get("/")
def bank_accounts_home():
    return render_template("coming_soon.html")