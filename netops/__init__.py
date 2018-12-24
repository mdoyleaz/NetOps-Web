# netops_web/__init__.py

# Flask Imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

# Local Imports
from config import app_config

# Database variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from .models import user_datastore, User

    security = Security(app, user_datastore)

    db.init_app(app)
    migrate = Migrate(app, db)

    Bootstrap(app)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .network import network as network_blueprint
    app.register_blueprint(network_blueprint)

    from .switches import switches as switches_blueprint
    app.register_blueprint(switches_blueprint)

    return app
