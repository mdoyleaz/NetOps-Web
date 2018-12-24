# netops/admin/__init__.py

from .. import db

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views
