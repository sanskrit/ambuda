import code
import textwrap
from fabric.api import *


PROJECT_NAME = 'ambuda'


def dump_to_file(data, filename):
    """Dump some data to a file. This is a helper function.

    :param data: the data to dump
    :param filename: name of the file to dump to
    """
    data = textwrap.dedent(data).lstrip()
    with open(filename, 'w') as f:
        f.write(data)


@task
def blueprint(name):
    """Create a blueprint and some common modules.

    Modules include:
    - ``forms.py`` for forms.
    - ``models.py`` for models.
    - ``views.py`` for views. This creates a blueprint and routes an
      index view.

    In addition, this function creates an index template at
    ``ambuda/templates/<name>/index.html``.

    :param name: the blueprint name
    """
    local('mkdir ambuda/{0}'.format(name))
    local('mkdir ambuda/templates/{0}'.format(name))
    local('touch ambuda/templates/{0}/index.html'.format(name))
    local('touch ambuda/{0}/__init__.py'.format(name))

    forms_data = """
    from flask.ext.wtf import Form
    """

    models_data = """
    from ambuda import db
    from ambuda.models import Base
    """

    views_data = """
    from flask import Blueprint, render_template

    bp = Blueprint('{0}', __name__, url_prefix='/{0}')


    @bp.route('/')
    def index():
        return render_template('{0}/index.html')
    """.format(name)

    dump_to_file(forms_data, 'ambuda/{0}/forms.py'.format(name))
    dump_to_file(models_data, 'ambuda/{0}/models.py'.format(name))
    dump_to_file(views_data, 'ambuda/{0}/views.py'.format(name))


@task
def init_project(name):
    """Replace all instances of ``'ambuda'`` with ``name``.

    This does not rename the top-level folder (``flask-ambuda``).

    If ``name`` doesn't conflict with any other terms, you can run this
    command again with no ill effects. When run this way, the command
    will replace all instances of the old name with ``name``.

    :param name: the new project name
    """
    command = """mv ambuda {0};
        find . -name "*.py" -print0 |
        xargs -0 sed -i s/ambuda/{0}/g
        """.format(name)
    local(command)


@task
def server():
    local('python runserver.py')


@task
def shell():
    """Create an interactive shell with some useful locals.

    Locals include:
    - ``app``, the application instance
    - ``db``, the Flask-SQLAlchemy database instance
    - all of the models that subclass `db.Model`.
    """

    # Banner, which is displayed at the beginning of the shell session
    banner = """
    {1}~~~~~~
    {0} shell
    {1}~~~~~~
    """.format(PROJECT_NAME, '~' * len(PROJECT_NAME))

    # Locals, which are injected into the shell contetx
    from ambuda import app, db
    context = db.Model._decl_class_registry.copy()
    context.update(dict(
        app=app,
        db=db
    ))

    code.interact(banner, local=context)


# Namespaces
import auth
