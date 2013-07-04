import sqlalchemy.exc
from flask import flash, redirect, render_template as render, url_for


from bodha import app, db
from bodha.models import *


@app.route('/')
def index():
    projects = Project.query.all()
    return render('index.html', projects=projects)


@app.route('/projects/')
def project_list():
    projects = Project.query.all()
    return render('project_list.html', projects=projects)


@app.route('/projects/<slug>')
def project(slug):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        flash("Sorry, we couldn't find project '%s'." % slug, 'error')
        return redirect(url_for('project_list'))

    return render('project.html', project=_project)


@app.route('/projects/<slug>/<segment>')
def segment(slug, segment=None):
    return render('segment.html')
