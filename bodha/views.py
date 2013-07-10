import random

import sqlalchemy.exc
from flask import flash, redirect, render_template as render, request, url_for
from flask.ext.security.decorators import roles_required
from flask.ext.uploads import configure_uploads, UploadSet, IMAGES

from bodha import app, db
from bodha.forms import ImagesForm, SegmentEditForm
from bodha.models import *


images = UploadSet('img', IMAGES)
GET_POST = ['GET', 'POST']
STATUS = {}


@app.context_processor
def upload_sets():
    return {
        'images': images
    }


@app.before_first_request
def status_enum():
    for s in Status.query.all():
        STATUS[s.name] = s


# Helper functions
# ~~~~~~~~~~~~~~~~
def missing_project(slug):
    flash("Sorry, we couldn't find \"%s\"." % slug, 'error')
    return redirect(url_for('project_list'))


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
        return missing_project(slug)

    return render('project.html', project=_project)


def segment_data(project_id, id=None):
    """

    :param project_id:
    :param id:
    """
    if id:
        try:
            return Segment.query.filter(Segment.id==id).one()
        except sqlalchemy.exc.SQLAlchemyError:
            return None

    q = Segment.query.filter(Segment.project_id==project_id)
    count = q.count()
    return q.offset(random.randrange(count)).first()


@app.route('/projects/<slug>/edit/', methods=GET_POST)
@app.route('/projects/<slug>/edit/<int:id>', methods=GET_POST)
def segment_edit(slug, id=None):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return missing_project(slug)

    _segment = segment_data(_project.id, id)

    form = SegmentEditForm()
    if _segment.revisions:
        form.content.data = _segment.revisions[-1].content

    if form.validate_on_submit() and _segment is not None:
        # Create a new revision. `index` is populated automatically.
        rev = Revision(
            content=form.content.data,
            status_id=None,
            segment_id=_segment.id
        )
        _segment.revisions.append(rev)

        # If marked as complete, change the segment status
        if form.complete.data:
            pass  # TODO

        db.session.commit()
        flash('Saved!', 'success')

    return render('segment.html', form=form,
                  project=_project,
                  segment=_segment)


@app.route('/projects/<slug>/upload', methods=['GET', 'POST'])
@roles_required('admin')
def upload_segments(slug):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return missing_project(slug)

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
