import os

DEBUG = True
SECRET_KEY = 'secret'

# flask-assets
# ------------
ASSETS_DEST = 'bodha/static'

# flask-security
# --------------
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '$2a$10$WyxRXkzAICMHgmqhMGTlJu'
SECURITY_CHANGEABLE = True
SECURITY_REGISTERABLE = True
SECURITY_CHANGE_URL = '/change'
SECURITY_LOGIN_USER_TEMPLATE = 'users/login.html'

# flask-sqlalchemy
# ----------------
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


# Uploads
# ~~~~~~~
UPLOADS_DEFAULT_DEST = os.path.expanduser('~/www/bodha/data')
