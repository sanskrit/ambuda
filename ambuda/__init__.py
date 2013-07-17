from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.markdown import Markdown
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('development.config')

# Assets
assets = Environment(app)
assets.url = '/static'
assets.directory = app.config['ASSETS_DEST']

less = Bundle('less/base.less', filters='less', output='gen/style.css')
assets.register('all-css', less)

js = Bundle('js/ambuda.js', output='gen/scripts.js')
assets.register('all-js', js)

# Database
db = SQLAlchemy(app)
import models
db.create_all()



# Markdown
Markdown(app)


# Security
datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, datastore)


# Admin
import admin


# Debug toolbar
if app.config['DEBUG']:
    from flask.ext.debugtoolbar import DebugToolbarExtension as DTE
    toolbar = DTE(app)


# Endpoints
import views


# Setup
import setup
