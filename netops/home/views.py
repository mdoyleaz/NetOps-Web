# netops/home/views.py

# External Imports
from flask import render_template
from flask_security import login_required, current_user

# Local Imports
from . import home

@home.route('/')
@login_required
def homepage():
    """
    Renders Homepage template for '/' path
    """
    abc = "French"

    return render_template('home/index.html', title='Home', abc=abc)
