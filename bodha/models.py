# -*- coding: utf-8 -*-
"""
    bodha.models
    ~~~~~~~~~~~~

    Models for a Wiki-like interface

    :license: MIT and BSD
"""

from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from bodha import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Status(Base):
    name = db.Column(db.String)


class Flag(Base):
    name = db.Column(db.String)


class Project(Base):
    #: Project title
    title = db.Column(db.String)
    #: How the project appears in URLs
    slug = db.Column(db.String, unique=True)
    #: Path to an instructions template
    instructions = db.Column(db.String, unique=True)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: Project status
    status_id = db.Column(db.ForeignKey('status.id'))

    status = db.relationship('Status', backref='projects')


class Segment(Base):
    #: Filepath to the corresponding image
    image_path = db.Column(db.String, unique=True)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: The corresponding `Project`
    project_id = db.Column(db.ForeignKey('project.id'), index=True)
    #: Project status
    status_id = db.Column(db.ForeignKey('status.id'))

    project = db.relationship('Project', backref='segments')
    status = db.relationship('Status', backref='segments')


class Revision(Base):
    #: Revision content
    content = db.Column(db.UnicodeText)
    #: Any notes the user left on this revision
    notes = db.Column(db.UnicodeText, nullable=True)
    #: Revision number. Higher numbers are more recent.
    index = db.Column(db.Integer, default=0, index=True)
    #: Time created
    created = db.Column(db.DateTime, default=datetime.utcnow)
    #: The corresponding `Flag`
    flag_id = db.Column(db.ForeignKey('flag.id'), index=True)
    #: The corresponding `Segment`
    segment_id = db.Column(db.ForeignKey('segment.id'), index=True)

    flag = db.relationship('Flag', backref='revisions')
    segment = db.relationship('Segment', backref='revisions')
