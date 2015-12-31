
# Skeleton definition for the app, which must be defined before
# the models
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///webcatalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mkd89$lpkkbeshuretochangeme'
# uploaded images should not have more than 2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

db = SQLAlchemy(app)


CsrfProtect(app)
