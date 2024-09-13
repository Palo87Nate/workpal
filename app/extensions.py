#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

#initialise extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()