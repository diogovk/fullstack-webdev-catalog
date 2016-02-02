from app import app
from flask_wtf import Form
from wtforms import TextField, FileField, HiddenField, validators
from helpers import get_image_extension
from flask import request


class NewItemForm(Form):
    name = TextField('Title', [
        validators.Length(min=3, max=128),
        validators.DataRequired()
        ])
    description = TextField('Title', [])
    image_file = FileField('Image', [])
    category_id = HiddenField('Category ID', [])

    def validate_image_file(form, field):
        # This field is optional, so empty is considered valid
        if not field.data:
            return
        extension = get_image_extension(field.data.filename)
        if extension and extension not in app.config['ALLOWED_IMG_EXTENSIONS']:
            raise validators.ValidationError(
                    "The uploaded image format is invalid")
        if field.data.filename and not request.files[form.image_file.name]:
            raise validators.ValidationError(
                    "Couln't find the file in form submission")
