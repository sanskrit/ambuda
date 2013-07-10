from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('development.config')

# Assets
assets = Environment(app)
assets.url = '/static'
assets.directory = app.config['ASSETS_DEST']

less = Bundle('less/base.less', filters='less', output='gen/style.css', depends=['a'])
assets.register('all-css', less)

# Database
db = SQLAlchemy(app)
import models
db.create_all()


# Security
datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, datastore)


# Admin
import admin


# Endpoints
import views


# Setup
import setup
