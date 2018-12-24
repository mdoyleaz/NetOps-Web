# netops/network/__init__.py

from flask import Blueprint

network = Blueprint('network', __name__)

from . import views
