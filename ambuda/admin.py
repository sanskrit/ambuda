from flask import current_app as app, redirect
from flask.ext.admin import (Admin, BaseView as _BaseView, AdminIndexView,
                             expose)
from flask.ext.admin.contrib.sqla import ModelView as _ModelView
from flask.ext.admin.contrib.sqla.form import AdminModelConverter
from flask.ext.admin.model.form import converts
from flask.ext.security import current_user

from wtforms import fields
from wtforms.validators import ValidationError

import models

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


class EnumSelectField(fields.SelectField):
    def __init__(self, model, **kw):
        super(EnumSelectField, self).__init__(**kw)
        self.model = model
        self.coerce = lambda x: x

    @property
    def data(self):
        return self.model.from_string(self._data)

    @data.setter
    def data(self, data):
        if data is None:
            self._data = None
        else:
            self._data = data.value

    def iter_choices(self):
        for key, description in self.model:
            yield (key, description, key == self._data)

    def process_formdata(self, valuelist):
        self._data = valuelist[0]

    def pre_validate(self, form):
        if self.data is not None:
            for key, description in self.model:
                if self._data == key:
                    break
            else:
                raise ValidationError(self.gettext(u'Not a valid choice'))


class ModelConverter(AdminModelConverter):

    @converts('DeclEnumType')
    def conv_DeclEnumType(self, column, field_args, **extra):
        return EnumSelectField(model=column.type.enum, **field_args)


class BaseView(AuthMixin, _BaseView):
    pass


class ModelView(AuthMixin, _ModelView):
    model_form_converter = ModelConverter


# Custom views
# ------------
class ProjectView(ModelView):
    column_list = ['id', 'name', 'slug', 'status', 'created']
    form_columns = ['name', 'slug', 'status', 'introduction', 'instructions']


class SegmentView(ModelView):
    column_list = ('id', 'project', 'image_path', 'status')


class UserView(ModelView):
    column_exclude_list = form_excluded_columns = ('password',)


# Admin setup
# -----------
admin = Admin(name='Index', index_view=AppIndexView())

admin.add_view(ProjectView(models.Project, models.db.session,
                           category='Projects',
                           name='Project list'))
admin.add_view(SegmentView(models.Segment, models.db.session,
                           category='Projects',
                           name='Segments'))
admin.add_view(ModelView(models.Revision, models.db.session,
                         category='Projects',
                         name='Revisions'))
admin.add_view(UserView(models.User, models.db.session,
                        category='Auth',
                        name='Users'))
admin.add_view(ModelView(models.Role, models.db.session,
                         category='Auth',
                         name='Roles'))
