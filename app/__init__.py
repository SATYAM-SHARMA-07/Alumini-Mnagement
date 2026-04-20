"""Application factory and extension initialization."""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.admin_routes import admin_bp
    from app.routes.alumni_routes import alumni_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.events_routes import events_bp
    from app.routes.mentorship_routes import mentorship_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(alumni_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(mentorship_bp)

    with app.app_context():
        db.create_all()

    return app
