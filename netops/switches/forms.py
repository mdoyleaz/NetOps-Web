from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, PasswordField, SelectField, StringField, SubmitField, \
    ValidationError
from wtforms.validators import DataRequired, IPAddress


class AddSwitchForm(FlaskForm):
    """
    Form to add a switch to the database
    """

    name = StringField("Switch Label *", validators=[DataRequired()])
    os = SelectField("Operating System*", choices=[
                     ('cisco_nxos', 'Cisco NX-OS'), ('cisco_ios', 'Cisco IOS')])
    ip = StringField("Switch IP *", validators=[IPAddress()])
    username = StringField("SSH Username *", validators=[DataRequired()])
    password = PasswordField("SSH Password *", validators=[DataRequired()])
    secret = PasswordField("Enable Secret (Optional)")
    submit = SubmitField("Submit")
