# netops/utils/auth.py

# Extra Imports
import string
import random

# Flask-Security Imports
from flask_security.utils import encrypt_password
from flask_security.registerable import register_user

# Local Imports
from .. import db
from ..models import user_datastore


def add_user(user, role):
    """
    Adds user to the database
    """

    user['password'] = encrypt_password(user['password'])
    user_datastore.create_user(**user)

    role = user_datastore.find_role(role)
    user_datastore.add_role_to_user(user['email'], role)

    db.session.commit()


def change_password(user):
    """
    Changes specified users password
    """

    password = password_generator()
    user.password = encrypt_password(password)

    db.session.commit()

    return password


def change_role(user, role):
    """
    Changes users role
    """

    role = user_datastore.find_role(role)

    user_datastore.remove_role_from_user(user, user.roles[0])
    user_datastore.add_role_to_user(user, role)


def password_generator():
    """
    Generates Password
    """

    generated_pass = ''.join(random.sample(
        string.ascii_letters + string.digits + string.punctuation, 16))

    return generated_pass
