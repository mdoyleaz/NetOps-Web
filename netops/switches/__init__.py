# netops/switches/__init__.py

from .. import db

from flask import Blueprint

switches = Blueprint('switches', __name__)

from . import views
