from flask_wtf import FlaskForm

from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, IPAddress


class IpCalcForm(FlaskForm):
    """
    Form for IPCalc
    """

    ip_address = StringField("Subnet", validators=[DataRequired(), IPAddress()])
    prefix = IntegerField("Prefix (ex. /24)")
    submit = SubmitField("Submit")
