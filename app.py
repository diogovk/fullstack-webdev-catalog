
# App configuration and setup
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from oauth2client.client import flow_from_clientsecrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mkd89$lpkkbeshuretochangeme'
# uploaded images should not have more than 2MB and should be of a
# known extension
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['IMAGE_FOLDER'] = './static/images'
app.config['ALLOWED_IMG_EXTENSIONS'] = set(['png', 'PNG', 'jpg', 'JPG'])
# These methods should have CSRF protection by default
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']

# basic database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///webcatalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# start CSRF protection
CsrfProtect(app)
