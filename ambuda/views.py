import os
import random
from zipfile import ZipFile

import sqlalchemy.exc
from flask import (current_app as app, flash, redirect, render_template as
                    render, url_for, Blueprint)
from flask.ext.security import current_user
from flask.ext.security.decorators import roles_required
from flask.ext.uploads import configure_uploads, UploadSet, IMAGES

from ambuda.forms import ImagesForm, SegmentEditForm
from ambuda.models import *


images = UploadSet('img', IMAGES)
GET_POST = ['GET', 'POST']
STATUS = {}

site = Blueprint('site', __name__, template_folder='templates')

@site.context_processor
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


def get_project(slug):
    """Fetch a project.

    :param slug: the project slug
    """
    try:
        return Project.query.filter(Project.slug==slug).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return None


def get_segment(project_id, id):
    """Fetch a segment.

    :param project_id:
    :param id:
    """
    try:
        return Segment.query.filter(Segment.id==id).one()
    except sqlalchemy.exc.SQLAlchemyError:
        return None


def random_segment(project_id):
    """Fetch a random segment from the project.

    :param project_id: the project ID
    """
    q = Segment.query.filter(Segment.project_id==project_id)
    count = q.count()
    return q.offset(random.randrange(count)).first()


# View functions
# ~~~~~~~~~~~~~~
@site.route('/')
def index():
    if current_user.is_authenticated():
        return render('index-user.html')
    else:
        return render('index-splash.html')


@site.route('/about')
def about():
    return render('about.html')


@site.route('/how-to/proofread')
def proofreading():
    return render('how-to/proofread.html')


@site.route('/projects/')
def project_list():
    projects = Project.query.all()
    return render('project_list.html', projects=projects)


@site.route('/projects/<slug>/')
def project(slug):
    _project = get_project(slug)
    if _project is None:
        return missing_project(slug)

    return render('project.html', project=_project)


@site.route('/projects/<slug>/edit/', methods=GET_POST)
@site.route('/projects/<slug>/edit/<int:id>', methods=GET_POST)
def segment_edit(slug, id=None):
    _project = get_project(slug)
    if _project is None:
        return missing_project(slug)

    if id is None:
        new_id = random_segment(_project.id).id
        return redirect(url_for('segment_edit', slug=slug, id=new_id))

    _segment = get_segment(_project.id, id)
    if _segment is None:
        return redirect(url_for('project', slug=slug))

    form = SegmentEditForm()
    if _segment.revisions:
        form.content.data = _segment.revisions[-1].content

    if form.validate_on_submit():
        # Create a new revision. `index` is populated automatically.
        new_status = Status.next(_segment.status)
        rev = Revision(
                content=form.content.data,
                status=new_status,
                segment_id=_segment.id
                )
        _segment.status = new_status
        _segment.revisions.append(rev)

        db.session.commit()
        flash('Saved!', 'success')

        # If marked as complete, show a new segment
        if form.complete.data:
            new_id = random_segment(_project.id).id
            return redirect(url_for('segment_edit', slug=slug, id=new_id))

    return render('segment.html', form=form,
            project=_project,
            segment=_segment)


@site.route('/projects/<slug>/upload', methods=['GET', 'POST'])
@roles_required('admin')
def upload_segments(slug):
    """
    Upload segments to the given project. Segments are bundled in a
    single zip file.

    :param slug: the project slug
    """
    _project = get_project(slug)
    if _project is None:
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


