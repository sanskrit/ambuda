import os

DEBUG = True
SECRET_KEY = 'secret'

# flask-assets
# ------------
ASSETS_DEST = 'ambuda/static'

# flask-debugtoolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

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
development_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(development_dir)
sqlalchemy_path = os.path.join(project_dir, 'test.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % sqlalchemy_path


# Uploads
# ~~~~~~~
UPLOADS_DEFAULT_DEST = os.path.expanduser('~/projects/ambuda/data')
