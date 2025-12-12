from flask import render_template
from . import accounts_bp

@accounts_bp.get("/")
def accounts_home():
    return render_template("coming_soon.html")