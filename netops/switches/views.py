# netops/switches/views.py

# Flask Imports
from flask import flash, redirect, render_template, request, url_for

# Flask-Security Imports
from flask_security import roles_accepted

# Local Imports
from . import switches, db
from .forms import AddSwitchForm
from ..models import User, Switch

# Utility Imports
from ..utils import database


# Switch Views
@switches.route('/switches/', methods=['GET'])
@roles_accepted('admin', 'user')
def list():
    switches = database.query_database(Switch)

    return render_template('switches/switch_list.html',
                           switches=switches, title="Switches")


@switches.route('/switches/add', methods=['GET', 'POST'])
@roles_accepted('admin', 'tech')
def add():
    """"
    Adds a new location to the Database
    """

    form = AddSwitchForm()
    if form.validate_on_submit():
        form_dict = request.form.to_dict()

        database.add_item(Switch, form_dict)

        flash('{} -- Added succesfully'.format(form_dict['name']), 'success')

        return redirect(url_for('switches.list'))

    return render_template('forms.html',
                           form=form, title="Add Switch")


@switches.route('/switches/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin')
def edit(id):

    switch = Switch.query.get_or_404(id)

    form = AddSwitchForm(obj=switch)

    if form.validate_on_submit():
        db.session.commit()

        flash(f"{switch.name} -- Modified Successfully", 'success')

        return redirect(url_for('switches.list'))

    return render_template('forms.html', form=form, title=f"Edit {switch.name}")


@switches.route('/switches/delete/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin')
def modify_deleted(id):
    """
    Marks deleted entry in 'Switch', to 'deleted=True'
    """

    switch = Switch.query.get_or_404(id)

    database.modify_status(switch)

    return redirect(url_for('switches.list'))
