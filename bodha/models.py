# -*- coding: utf-8 -*-
"""
    bodha.models
    ~~~~~~~~~~~~

    Models for a Wiki-like interface

    :license: MIT and BSD
"""

from datetime import datetime

from flask.ext.principal import Permission, RoleNeed
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list

from bodha import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Status(Base):
    name = db.Column(db.String)

    def __unicode__(self):
        return self.name


class Project(Base):
    #: Project title
    name = db.Column(db.String)
    #: How the project appears in URLs
    slug = db.Column(db.String(30), unique=True)
    #: Path to an instructions template
    instructions = db.Column(db.String, unique=True)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: Project status
    status_id = db.Column(db.ForeignKey('status.id'))

    status = db.relationship('Status', backref='projects')

    def __unicode__(self):
        return self.slug


class Segment(Base):
    #: Filepath to the corresponding image
    image_path = db.Column(db.String, unique=True)
    #: Number of times marked complete
    num_completions = db.Column(db.Integer, default=0)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: The corresponding `Project`
    project_id = db.Column(db.ForeignKey('project.id'), index=True)
    #: Project status
    status_id = db.Column(db.ForeignKey('status.id'))

    project = db.relationship('Project', backref='segments')
    status = db.relationship('Status', backref='segments')
    revisions = db.relationship('Revision', backref='segment',
                                collection_class=ordering_list('index'))

    def __unicode__(self):
        return self.image_path


class Revision(Base):
    #: Revision content
    content = db.Column(db.UnicodeText)
    #: Revision number. Higher numbers are more recent.
    index = db.Column(db.Integer, default=0, index=True)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: The corresponding `Segment`
    segment_id = db.Column(db.ForeignKey('segment.id'), index=True)
    #: Project status
    status_id = db.Column(db.ForeignKey('status.id'))

    # -- 'Segment' backref is addressed above.
    status = db.relationship('Status', backref='revisions')


# Authentication
# --------------
class UserRoleAssoc(db.Model):
    __tablename__ = 'user_role_assoc'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.ForeignKey('role.id'), primary_key=True)


class User(Base, UserMixin):
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)

    roles = db.relationship('Role', secondary='user_role_assoc',
                            backref='users')

    def can_edit(self, project):
        return self.is_admin()

    def has_role(self, role):
        p = Permission(RoleNeed(role))
        return p.can()

    def is_admin(self):
        return self.has_role('admin')


class Role(Base, RoleMixin):
    name = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Role(%s, %s)>' % (self.id, self.name)
