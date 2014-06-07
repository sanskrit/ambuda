from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.markdown import Markdown
from flask.ext.security import Security, SQLAlchemyUserDatastore

import admin
import models
import views

assets = Environment()

less = Bundle('less/base.less', filters='less', output='gen/style.css')
assets.register('all-css', less)

js = Bundle('js/ambuda.js', output='gen/scripts.js')
assets.register('all-js', js)

datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)


def create_app(name, config_path):
    app = Flask(name, static_folder='ambuda/static')
    app.config.from_object(config_path)

    admin.admin.init_app(app)

    assets.init_app(app)
    assets.app = app
    assets.url = '/static'
    assets.directory = app.config['ASSETS_DEST']

    models.db.init_app(app)

    security = Security(app, datastore)

    Markdown(app)

    # File uploading
    views.configure_uploads(app, (views.images,))

    # Debug toolbar
    if app.config['DEBUG']:
        from flask.ext.debugtoolbar import DebugToolbarExtension as DTE
        toolbar = DTE(app)

    app.register_blueprint(views.site)
    return app
