from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

"""App factory and extensions initialization.

Defines `db` and `login_manager` instances and the `create_app`
factory that registers blueprints and initializes extensions.
"""

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Create and configure the Flask application.

    Returns the Flask app with extensions (SQLAlchemy, LoginManager)
    initialized and blueprints registered.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from . import models
    from .auth import auth
    from .routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app