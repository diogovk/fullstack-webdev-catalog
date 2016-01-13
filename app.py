
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
app.config['IMAGE_FOLDER'] = './static/images'
app.config['ALLOWED_IMG_EXTENSIONS'] = set(['png', 'PNG', 'jpg', 'JPG'])
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']

db = SQLAlchemy(app)


CsrfProtect(app)
