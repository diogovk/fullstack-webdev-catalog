from flask_wtf import Form
from wtforms import TextField, validators


class NewItemForm(Form):
    name = TextField('Title', [
        validators.Length(min=3, max=128),
        validators.DataRequired()
        ])
