from flask.ext.wtf import Form, Required
from wtforms import FileField


class ImagesForm(Form):
    path = FileField("Segments", [Required()])
