import os
import random
from zipfile import ZipFile

import sqlalchemy.exc
from flask import flash, redirect, render_template as render, url_for
from flask.ext.security import current_user
from flask.ext.security.decorators import roles_required
from flask.ext.uploads import configure_uploads, UploadSet, IMAGES

from ambuda import app, db
from ambuda.forms import ImagesForm, SegmentEditForm
from ambuda.models import *


images = UploadSet('img', IMAGES)
GET_POST = ['GET', 'POST']
STATUS = {}


@app.context_processor
def upload_sets():
    return {
        'images': images,
        'Status': Status
    }


# Helper functions
# ~~~~~~~~~~~~~~~~
def missing_project(slug):
    flash("Sorry, we couldn't find \"%s\"." % slug, 'error')
    return redirect(url_for('project_list'))


@app.route('/')
def index():
    print images.__dict__
    print images.default_dest
    if current_user.is_authenticated():
        return render('index-user.html')
    else:
        return render('index-splash.html')


@app.route('/about')
def about():
    return render('about.html')


@app.route('/how-to/proofread')
def proofreading():
    return render('how-to/proofread.html')


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


def random_segment(project_id):
    """Fetch a random segment from the project.

    :param project_id: the project ID
    """
    q = Segment.query.filter(Segment.project_id==project_id)
    count = q.count()
    return q.offset(random.randrange(count)).first()


def segment_data(project_id, id=None):
    """

    :param project_id:
    :param id:
    """
    try:
        return Segment.query.filter(Segment.id==id).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return None


@app.route('/projects/<slug>/edit/', methods=GET_POST)
@app.route('/projects/<slug>/edit/<int:id>', methods=GET_POST)
def segment_edit(slug, id=None):
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return missing_project(slug)

    if id is None:
        new_id = random_segment(_project.id).id
        return redirect(url_for('segment_edit', slug=slug, id=new_id))

    _segment = segment_data(_project.id, id)

    form = SegmentEditForm()
    if _segment.revisions:
        form.content.data = _segment.revisions[-1].content

    if form.validate_on_submit() and _segment is not None:
        # Create a new revision. `index` is populated automatically.
        new_status = Status.next(_segment.status)
        rev = Revision(
            content=form.content.data,
            status=new_status,
            segment_id=_segment.id
        )
        _segment.status = new_status
        _segment.revisions.append(rev)

        # If marked as complete, show a new segment
        if form.complete.data:
            new_id = random_segment(_project.id).id
            return redirect(url_for('segment_edit', slug=slug, id=new_id))

        db.session.commit()
        flash('Saved!', 'success')

    return render('segment.html', form=form,
                  project=_project,
                  segment=_segment)


@app.route('/projects/<slug>/upload', methods=['GET', 'POST'])
@roles_required('admin')
def upload_segments(slug):
    """
    Upload segments to the given project. Segments are bundled in a
    single zip file.

    :param slug: the project slug
    """
    try:
        _project = Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return missing_project(slug)

    form = ImagesForm()
    if form.validate_on_submit():
        z = ZipFile(form.path.data)

        # Extract all images to <images>/<slug>
        dir_path = images.path(slug)
        z.extractall(dir_path)

        # Create `Segment` objects for each image.
        filenames = [os.path.join(slug, f) for f in z.namelist()]
        for name in filenames:
            db.session.add(Segment(
                image_path=name,
                project_id=_project.id,
                status=Status.proofreading_1
            ))
        db.session.commit()

        flash('Uploaded %s images.' % len(filenames))

    return render('upload-segments.html', form=form)


configure_uploads(app, (images,))
