# netops/utils/database.py

from datetime import datetime
from getpass import getpass

from flask import flash
from flask_security.utils import encrypt_password

from .. import db
from ..models import User, user_datastore

def first_start():
    """
    Script to build initial database objects
    """

    print("Checking for Database")

    if not User.query.first():
        try:
            print("Database not found!\n")
            print("Creating Database")

            # Create roles
            admin_role = user_datastore.find_or_create_role('admin')
            user_datastore.find_or_create_role('user')

            # Create 'First' user
            email = input("Enter admin account email: ")

            password_match = False
            while not password_match:
                password = getpass("Enter admin password: ")
                password_again = getpass("Re-enter admin password: ")

                if password_again != password:
                    print("Passwords do not match, please try again.\n")
                else:
                    password_match = True

            user = user_datastore.create_user(
                email=email, password=encrypt_password(password))
            user_datastore.add_role_to_user(user, admin_role)

            db.session.commit()

            print("\n#################################")
            print("Database created successfully\n")
            print(f"Default login:" \
            f"\n Username: {email}" \
            f"\n Password: {password}")
            print("\n#################################\n")
        except Exception as e:
            print(f"Creation of database FAILED :: {e}")
    else:
        print("Database found!\nStarting ServerHub Netops Web\n")

def modify_status(db_query, user=False):
    """
    All tables have a name column, except for user;
    Use:
        Query the database and pass it in as a parameter;
    Requires:
        db_query - A query must be past to remove;
    """
    if user:
        if db_query.active:
            db_query.active = False
            db_query.deactivated_at = datetime.now()

            flash("{} -- Disabled".format(db_query.email), 'success')
        else:
            db_query.active = True
            db_query.reactivated_at = datetime.now()

            flash("{} -- Reactivated".format(db_query.email), 'success')
    else:
        if db_query.deleted:
            db_query.deleted = False
            db_query.deleted_at = None

            flash("{} -- Deleted succesfully".format(db_query.name), 'success')
        else:
            db_query.deleted = True
            db_query.deleted_at = datetime.now()

            flash("{} -- Restored succesfully".format(db_query.name), 'success')

    db.session.commit()


def query_choices(db_model, required=False):
    """
    Generates form options;
    Requires:
        db_model - A database model must be past to query;
    """
    choices_query = [(item.name, item.name.capitalize())
                     for item in db_model.query.filter_by(
        deleted=False).order_by(db_model.name).all()]

    if not required:
        choices_query.append((None, 'None'))

    return choices_query


def query_database(db_model, deleted=False, **kwargs):
    """
    Query options
    Requires:
        'db_model': Pass the model that you would like to query;
    Optional:
        'deleted': True - Shows only deleted items;
                   False - Shows only non deleted items;
                   'all' - Shows all items in table;
        '**kwargs': Accepted dynamic filtering, you may pass filters through as
                    'name=name_example';
    """
    try:
        if deleted is "all":
            query = db_model.query.filter_by(**kwargs).order_by(db_model.deleted).all()
        else:
            query = db_model.query.filter_by(deleted=deleted, **kwargs).all()
    except AttributeError:
        query = None

    return query

def add_item(db_model, form_dict):

    del form_dict['csrf_token']
    del form_dict['submit']

    db_item = db_model(**form_dict)

    db.session.add(db_item)
    db.session.commit()

    return
