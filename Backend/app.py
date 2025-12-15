import os
from flask import Flask, request, redirect
from Backend.config import DevelopmentConfig, TestingConfig, ProductionConfig
from Backend.extensions import db, migrate, login_manager, jwt
from Backend.blueprints.main import main_bp
from Backend.blueprints.api_v1 import api_v1_bp
from Backend.blueprints.api_v2 import api_v2_bp
from Backend.services.navigation import pop_nav, push_nav, EXCLUDED_ENDPOINTS
from Backend.services.message_service import MessageService
from Backend.auth import get_auth_strategy
from Backend.models import User
from Backend.blueprints.account import account_bp
from Backend.blueprints.auth import auth_bp
from Backend.blueprints.calculators import calculators_bp
from Backend.blueprints.contact import contact_bp
from Backend.blueprints.bank_accounts import bank_accounts_bp
from Backend.blueprints.budget import budget_bp
from Backend.blueprints.education import education_bp
from Backend.blueprints.retirement import retirement_bp
from Backend.blueprints.settings import settings_bp
from Backend.blueprints.pages import pages_bp
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app(config_name=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "Frontend", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "Frontend", "static")
    )

    # Config selection
    env = config_name or os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from Backend.models import User
        identity = jwt_data["sub"]
        return User.query.get(identity)

    # Services (DI)
    app.message_service = MessageService(db)

    # Auth strategy
    app.auth_strategy = get_auth_strategy(app)

    @app.before_request
    def check_maintenance_mode():
        if app.config.get("FEATURE_MAINTENANCE"):
            from flask import render_template
            return render_template("maintenance.html"), 503
        
    @app.before_request
    def track_navigation():
        # Skip excluded endpoints
        if request.endpoint in EXCLUDED_ENDPOINTS:
            return

        # Skip static files
        if request.path.startswith("/static/"):
            return

        # Skip API routes
        if request.path.startswith("/api/"):
            return

        push_nav(request.path)

    @app.route("/back")
    def go_back():
        previous = pop_nav()
        return redirect(previous)

        
    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
    app.register_blueprint(api_v2_bp, url_prefix="/api/v2") # for reference only, not currently used
    app.register_blueprint(account_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bank_accounts_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(calculators_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(education_bp)
    app.register_blueprint(retirement_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(pages_bp)

    # Add context processor
    @app.context_processor
    def inject_config():
        return dict(config=app.config)

    @app.context_processor
    def inject_globals():
        return {
            "config": app.config,
            "current_year": datetime.now().year
        }
    
    return app