from flask import Flask
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('development.config')


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
