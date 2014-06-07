from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, TextAreaField, validators


class ImagesForm(Form):
    path = FileField("Segments", [validators.Required()])


class SegmentEditForm(Form):
    content = TextAreaField('Content', [validators.Required()])
    in_progress = SubmitField('Save as "in progress"')
    complete = SubmitField('Save as "complete"')
