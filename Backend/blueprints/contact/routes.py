from flask import render_template
from . import contact_bp

@contact_bp.get("/")
def contact_home():
    return render_template("coming_soon.html")