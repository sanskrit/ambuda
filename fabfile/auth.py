from getpass import getpass
from fabric.api import *

from ambuda import app, datastore, db
from flask.ext.security.script import CreateUserCommand


def create_user(email=None):
    if email is None:
        email = prompt('Email:')
    password = getpass()

    with app.app_context():
        CreateUserCommand().run(email=email, password=password, active='y')
        return (email, password)


@task
def new_user(email=None):
    """Create a new user.

    :param email: the email address of the new account. If ``None``,
                  prompt for an email address.
    """
    create_user(email)


@task
def new_admin(email=None):
    """Create a new user and give the user the "admin" role.

    :param email: the email address of the new account. If ``None``,
                  prompt for an email address.
    """
    email, password = create_user(email)

    with app.app_context():
        datastore.find_or_create_role('admin')
        datastore.add_role_to_user(email, 'admin')
        db.session.commit()


@task
def new_role(name):
    """Create a new role.

    :param name: the role name
    """
    with app.app_context():
        datastore.find_or_create_role(name)
        db.session.commit()


@task
def add_role(email, name):
    """Give a user a role.

    :param email: the email address of the user
    :param name: the role name
    """
    with app.app_context():
        datastore.add_role_to_user(email, name)
        db.session.commit()
