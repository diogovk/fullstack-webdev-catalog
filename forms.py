from app import app
from flask_wtf import Form
from wtforms import TextField, FileField, HiddenField, validators
from helpers import get_image_extension
from flask import request


class NewItemForm(Form):
    """ Form used to create or edit a new Item """
    name = TextField('Title', [
        validators.Length(min=3, max=128),
        validators.DataRequired()
        ])
    description = TextField('Title', [])
    # image path in the filesystem
    image_file = FileField('Image', [])
    category_id = HiddenField('Category ID', [])

    def validate_image_file(form, field):
        '''
        Validates the image_file field.
        The request is considered valid if:
        * image_file is empty, since it's optional.
        * image file is of known image extension and the there's a file in the
            request.
        '''
        if not field.data:
            return
        extension = get_image_extension(field.data.filename)
        if extension and extension not in app.config['ALLOWED_IMG_EXTENSIONS']:
            raise validators.ValidationError(
                    "The uploaded image format is invalid")
        if field.data.filename and not request.files[form.image_file.name]:
            raise validators.ValidationError(
                    "Couln't find the file in form submission")
