from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY environment variable must be set. "
            "See .env.example for local development."
        )

    db.init_app(app)

    from app.admin import admin_bp
    from app.auth import auth_bp
    from app.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
