from flask import render_template
from flask import session
from . import main_bp

@main_bp.get("/")
def home():
    session["nav_stack"] = ["/"]
    return render_template("home.html")