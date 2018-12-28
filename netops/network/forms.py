from flask_wtf import FlaskForm

from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, IPAddress, Optional


class IpCalcForm(FlaskForm):
    """
    Form for IPCalc
    """

    subnet = StringField("Subnet", validators=[DataRequired(), IPAddress()])
    prefix = IntegerField("Prefix (ex. /24)")
    submit = SubmitField("Submit")

    split_prefix = IntegerField("Split Prefix into: ", validators=[Optional()])
    submit_split = SubmitField("Split")


class IpPingForm(FlaskForm):
    """
    Form to check status of IP address
    """

    ip_address = StringField("IP Address", validators=[
                             DataRequired(), IPAddress()])
    submit = SubmitField("Submit")
