

"""App factory and extensions initialization.

Defines `db` and `login_manager` instances and the `create_app`
factory that registers blueprints and initializes extensions.
"""

"""Create and configure the Flask application.

    Returns the Flask app with extensions (SQLAlchemy, LoginManager)
    initialized and blueprints registered.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app