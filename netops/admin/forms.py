# netops/admin/forms.py
from flask_wtf import FlaskForm

from flask_security import Security
from flask_security.forms import RegisterForm

from wtforms import StringField, SubmitField, SelectField, ValidationError, PasswordField
from wtforms.validators import DataRequired

from ..models import User, Role

class CreateUserForm(RegisterForm):
    """
    Form for ADMIN to create a new account
    """

    name = StringField('First/Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[])
    submit = SubmitField("Create User")

class EditUserForm(FlaskForm):
    """
    Form provided to edit users
    """

    email = StringField('Email')
    name = StringField('First/Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[])
    change_password = SubmitField("Change Password")
    submit = SubmitField('Submit')
