from flask import render_template, current_app, request, redirect
from . import settings_bp

@settings_bp.get("/")
def settings_home():
    return render_template("settings/index.html")

@settings_bp.post("/update")
def update_settings():
    for key in current_app.config:
        if key.startswith("FEATURE_"):
            current_app.config[key] = key in request.form
    return redirect("/settings")