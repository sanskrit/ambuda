import os

DEBUG = True
SECRET_KEY = 'secret'


# flask-security
# --------------
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '$2a$10$WyxRXkzAICMHgmqhMGTlJu'


# flask-sqlalchemy
# ----------------
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


# Uploads
# ~~~~~~~
UPLOADS_DEFAULT_DEST = os.path.expanduser('~/www/bodha/data')
