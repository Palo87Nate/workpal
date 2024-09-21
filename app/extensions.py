#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from mongoengine import connect

#initialise extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def init_extensions(app):
    """Initialize all the Flask extensions with the app instance."""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    connect(
        db=app.config['MONGODB_SETTINGS']['db'],
        host=app.config['MONGODB_SETTINGS']['host'],
        port=app.config['MONGODB_SETTINGS']['port']
    )