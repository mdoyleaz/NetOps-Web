# netops_web/models.py

# Standard Imports
from datetime import datetime
# Flask Imports
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

# Local Imports
from netops import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.now())
    deleted = db.Column(db.Boolean(), default=False)
    deleted_on = db.Column(db.DateTime())

# Authentication Models
class RolesUsers(Base):
    """
    User Roles Relational Table
    """

    __tablename__ = 'roles_users'

    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(Base, RoleMixin):
    """
    Models to store user roles
    """

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<Role id={self.id} Role={self.name}>'

class User(Base, UserMixin):
    """
    Model to store user details
    """

    __tablename__ = 'user'

    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(255))

    last_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(30))
    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(30))
    login_count = db.Column(db.Integer())

    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))


    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'


class Switch(Base):
    """
    Model to store switches
    """

    os = db.Column(db.String(128))
    ip = db.Column(db.String(16))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    secret = db.Column(db.String(255))

    def __repr__(self):
        return f'<Switch id={self.id} name={self.name}>'


class Logs(Base):
    """
    Logs switch activity
    """

    name = db.Column(db.String(255), index=True,
                     unique=True, default=datetime.now())
    email = db.Column(db.String(255), index=True)
    subnet = db.Column(db.String(20), index=True)
    switch = db.Column(db.String(120), index=True)
    notes = db.Column(db.String(255), index=True)

    def __repr__(self):
        return f'<Log id={self.id} name={self.name}>'



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
