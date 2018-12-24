# netops/admin/views.py

# Flask Imports
from flask import flash, redirect, render_template, url_for

# Flask-Security Imports
from flask_security import roles_required

# Local Imports
from . import admin, db
from .forms import CreateUserForm, EditUserForm
from ..models import User, Role, user_datastore

# Utility Imports
from ..utils import auth
from ..utils import database


@admin.route('/users', methods=['GET'])
@roles_required('admin')
def user_list():
    users = User.query.order_by(User.active.desc(), User.email).all()

    return render_template('admin/users.html', users=users, title="Users")


@admin.route('/createuser', methods=['GET', 'POST'])
@roles_required('admin')
def create_user():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """

    form = CreateUserForm()
    form.role.choices = database.query_choices(Role, required=True)[::-1]

    if form.validate_on_submit():
        user = form.to_dict()
        role = form.role.data

        auth.add_user(user, role)

        flash('Account Created Succesfully', 'success')

        return redirect(url_for('admin.user_list'))

    generated_pass = auth.password_generator()

    return render_template('/admin/create_user.html', register_user_form=form,
                           password=generated_pass, title='Create User')


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def modify_activation(id):
    """
    Modifies user status
    """

    user = user_datastore.get_user(id)
    database.modify_status(user, user=True)

    return redirect(url_for('admin.user_list'))


@admin.route('/users/modify/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_user(id):
    """
    Edit User Details
    """

    user = User.query.get_or_404(id)

    form = EditUserForm(obj=user)
    form.role.choices = database.query_choices(Role, required=True)[::-1]

    if form.change_password.data:
        new_password = auth.change_password(user)

        flash(f"{user.email}  -- New Password: {new_password}")

        return redirect(url_for('admin.edit_user', id=id))

    if form.validate_on_submit():
        if form.submit.data:
            user.name = form.name.data
            role = form.role.data

            if role is not user.roles[0]:
                auth.change_role(user, role)

        db.session.commit()

        flash("{} has been edited".format(user.email), 'success')

        return redirect(url_for('admin.user_list'))

    form.email.render_kw = {'disabled': 'disabled', 'value': user.email}
    form.role.data = user.roles[0]

    return render_template('/admin/modify_user.html', action="Edit",
                           form=form, title="Edit User")
