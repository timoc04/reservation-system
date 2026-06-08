from flask import Flask

from .config import Config
from .database import initialise_database


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    with app.app_context():
        initialise_database()

    from .routes import main
    from .auth_routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app