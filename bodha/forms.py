from flask.ext.wtf import Form, Required
from wtforms import FileField, SubmitField, TextAreaField


class ImagesForm(Form):
    path = FileField("Segments", [Required()])


class SegmentEditForm(Form):
    content = TextAreaField('Content', [Required()])
    in_progress = SubmitField('Save as "in progress"')
    complete = SubmitField('Save as "complete"')
