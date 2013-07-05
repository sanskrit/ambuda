from flask import redirect
from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.security import current_user


class AppIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        print current_user.email
        print 'roles:', current_user.roles
        if current_user.has_role('admin'):
            return self.render(self._template)
        else:
            return redirect('/')


admin = Admin(name='Index', index_view=AppIndexView())


# Attach to app
# -------------
from bodha import app
admin.init_app(app)
