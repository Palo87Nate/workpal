from flask import Flask
from .config import Config
from .extensions import *
from .routes import api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints (for routes)
    app.register_blueprint(api_blueprint)

    # Create tables before the first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
