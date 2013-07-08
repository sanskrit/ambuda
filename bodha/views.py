import sqlalchemy.exc
from flask import flash, redirect, render_template as render, url_for
from flask.ext.uploads import configure_uploads, UploadSet, IMAGES


from bodha import app, db
from bodha.forms import ImagesForm
from bodha.models import *


images = UploadSet('img', IMAGES)


@app.context_processor
def upload_sets():
    return {
        'images': images
    }


@app.route('/')
def index():
    projects = Project.query.all()
    return render('index.html', projects=projects)


@app.route('/projects/')
def project_list():
    projects = Project.query.all()
    return render('project_list.html', projects=projects)


@app.route('/projects/<slug>/')
def project(slug):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        flash("Sorry, we couldn't find project '%s'." % slug, 'error')
        return redirect(url_for('project_list'))

    return render('project.html', project=_project)


@app.route('/projects/<slug>/<int:id>')
def segment(slug, id=None):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
        _segment = Segment.query.filter(Segment.id==id).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return redirect(url_for('project_list'))

    return render('segment.html', project=_project, segment=_segment)


@app.route('/projects/<slug>/upload', methods=['GET', 'POST'])
def upload_segments(slug):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        flash("Sorry, we couldn't find project '%s'." % slug, 'error')
        return redirect(url_for('project_list'))

    form = ImagesForm()
    if form.validate_on_submit():
        file_objs = form.path.raw_data
        filenames = [images.save(f, folder=_project.slug) for f in file_objs]

        for name in filenames:
            db.session.add(Segment(
                image_path=name,
                project_id=_project.id,
                status_id=None
            ))
        db.session.commit()


        flash('Uploaded %s images.' % len(file_objs))
        success = True
    else:
        success = False
    return render('upload-segments.html', form=form,
                           success=success)


configure_uploads(app, (images,))
