from flask import render_template
from . import account_bp

@account_bp.get("/")
def account_home():
    return render_template("coming_soon.html")