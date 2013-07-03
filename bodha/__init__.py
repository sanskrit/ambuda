from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('development.config')


# Database
db = SQLAlchemy(app)
import models
db.create_all()

# Endpoints
import views
