import os

DEBUG = True
SECRET_KEY = 'secret'

# flask-assets
# ------------
ASSETS_DEST = 'ambuda/static'

# flask-security
# --------------
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '$2a$10$WyxRXkzAICMHgmqhMGTlJu'
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_LOGIN_USER_TEMPLATE = 'users/login.html'
SECURITY_REGISTER_USER_TEMPLATE = 'users/register.html'

# flask-sqlalchemy
# ----------------
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


# Uploads
# ~~~~~~~
UPLOADS_DEFAULT_DEST = os.path.expanduser('~/www/ambuda/data')
