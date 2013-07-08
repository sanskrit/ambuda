from flask import redirect
from flask.ext.admin import (Admin, BaseView as _BaseView, AdminIndexView,
                             expose)
from flask.ext.admin.contrib.sqlamodel import ModelView as _ModelView
from flask.ext.security import current_user

from bodha import app, db
from bodha import models


# Base classes
# ------------
class AuthMixin(object):

    def is_accessible(self):
        return current_user.has_role('admin')


class AppIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.has_role('admin'):
            return self.render(self._template)
        else:
            return redirect('/')


class BaseView(AuthMixin, _BaseView):
    pass


class ModelView(AuthMixin, _ModelView):
    pass


# Custom views
# ------------
class SegmentView(ModelView):
    column_list = form_excluded_columns = ('id', 'project', 'image_path',
                                           'status')


class UserView(ModelView):
    column_exclude_list = form_excluded_columns = ('password',)


# Admin setup
# -----------
admin = Admin(name='Index', index_view=AppIndexView())

admin.add_view(ModelView(models.Project, db.session,
                         category='Projects',
                         name='Project list'))
admin.add_view(SegmentView(models.Segment, db.session,
                           category='Projects',
                           name='Segments'))
admin.add_view(ModelView(models.Revision, db.session,
                         category='Projects',
                         name='Revisions'))
admin.add_view(UserView(models.User, db.session,
                        category='Auth',
                        name='Users'))
admin.add_view(ModelView(models.Role, db.session,
                         category='Auth',
                         name='Roles'))


admin.init_app(app)
