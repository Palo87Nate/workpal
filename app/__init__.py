#!/usr/bin/python3

from flask import Flask
from .config import Config
from .extensions import init_extensions
from .extensions import db
from .routes import api_blueprint
from .models import *

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    # Register blueprints (for routes)
    app.register_blueprint(api_blueprint)

    # Create tables before the first request
    with app.app_context():
        Documents.objects()

        db.create_all()

    return app
