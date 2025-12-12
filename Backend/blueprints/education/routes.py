from flask import render_template
from . import education_bp

@education_bp.get("/")
def education_home():
    return render_template("coming_soon.html")