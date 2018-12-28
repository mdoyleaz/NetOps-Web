# netops/network/views.py

# Flask Imports
from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required

# Local Imports
from . import network
from .forms import IpCalcForm, IpPingForm

# Utility Imports
from ..utils.ipcalc import IpCalcVerFour


@network.route('/ipcalc', methods=['GET', 'POST'])
@network.route('/ipcalc/subnet=<subnet>&prefix=<prefix>', methods=['GET', 'POST'])
@network.route('/ipcalc/subnet=<subnet>&prefix=<prefix>&split=<int:split_prefix>', methods=['GET', 'POST'])
@login_required
def ip_calc(subnet=None, prefix=None, split_prefix=0):
    """
    IPCalc Form
    """

    form = IpCalcForm()
    data = dict()

    if subnet and prefix:
        ip_calc = IpCalcVerFour(subnet, prefix)
        data['calc'] = ip_calc.__dict__()

    if form.validate_on_submit():
        subnet = form.subnet.data
        prefix = form.prefix.data

        split_prefix = form.split_prefix.data

        if split_prefix and split_prefix <= prefix:
            flash("Subnet must be greater than split prefix.", 'error')
            split_prefix = None

        return redirect(url_for('network.ip_calc', subnet=subnet,
                                prefix=prefix, split_prefix=split_prefix))

    form.subnet.data = subnet
    form.prefix.data = prefix

    if split_prefix:
        data['split'] = ip_calc.split_subnet(split_prefix)

    return render_template('network/ipcalc.html', form=form, data=data,
                           title="IP Calculator")


@network.route('/pinger', methods=['GET', 'POST'])
@network.route('/pinger/<ip_address>', methods=['GET', 'POST'])
@login_required
def pinger_tool(ip_address=None):
    """
    View creates a webpage to test status of IP Address
    """

    form = IpPingForm(obj=ip_address)

    if form.validate_on_submit():
        ip_address = form.ip_address.data

        return redirect(url_for('network.pinger_tool', ip_address=ip_address))

    form.ip_address.data = ip_address

    return render_template('forms.html', form=form, title="Pinger Tool")
