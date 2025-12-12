from flask import render_template
from . import retirement_bp

@retirement_bp.get("/")
def retirement_home():
    return render_template("coming_soon.html")