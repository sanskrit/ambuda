from flask import redirect
from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView as _ModelView
from flask.ext.security import current_user

from bodha import db
from bodha import models


class AuthMixin(object):

    def is_accessible(self):
        return current_user.has_role('admin')


class AppIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        print current_user.email
        print 'roles:', current_user.roles
        if current_user.has_role('admin'):
            return self.render(self._template)
        else:
            return redirect('/')


class AppView(AuthMixin, BaseView):
    pass


class ModelView(AuthMixin, _ModelView):
    pass


class UserView(ModelView):
    column_exclude_list = form_excluded_columns = ('password',)


admin = Admin(name='Index', index_view=AppIndexView())

admin.add_view(ModelView(models.Project, db.session,
                         category='Projects',
                         name='Project list'))
admin.add_view(ModelView(models.Segment, db.session,
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

# Attach to app
# -------------
from bodha import app
admin.init_app(app)
