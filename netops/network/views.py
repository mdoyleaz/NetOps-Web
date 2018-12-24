# netops/network/views.py

# Flask Imports
from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required

# Local Imports
from . import network
from .forms import IpCalcForm

# Utility Imports
from ..utils.ipcalc import IpCalcVerFour


@network.route('/ipcalc', methods=['GET', 'POST'])
@login_required
def ip_calc(subnet=None):
    """
    IPCalc Form
    """
    form = IpCalcForm()

    if form.validate_on_submit() or subnet:
        subnet = (form.ip_address.data, form.prefix.data)
        details = IpCalcVerFour(*subnet)
        ip_details = details.__dict__()


        return render_template('network/ipcalc.html', form=form,
                              data=ip_details, title="IP Calculator")

    return render_template('network/ipcalc.html', form=form, data=None,
                           title="IP Calculator")
