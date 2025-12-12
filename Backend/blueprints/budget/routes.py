from flask import render_template
from . import budget_bp

@budget_bp.get("/")
def budget_home():
    return render_template("coming_soon.html")