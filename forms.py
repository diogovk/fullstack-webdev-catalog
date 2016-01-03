from app import app
from flask_wtf import Form
from wtforms import TextField, FileField, validators
from helpers import get_image_extension
from flask import request

class NewItemForm(Form):
    name = TextField('Title', [
        validators.Length(min=3, max=128),
        validators.DataRequired()
        ])
    image_file = FileField('Image', [])

    def validate_image_file(form, field):
        extension = get_image_extension(field.data.filename)
        if extension and extension not in app.config['ALLOWED_IMG_EXTENSIONS']:
            raise validators.ValidationError(
                    "The uploaded image format is invalid")
        if field.data.filename and not request.files[form.image_file.name]:
            raise validators.ValidationError(
                    "Couln't find the file in form submission")
