#!/usr/bin/python2

from flask import request, render_template, redirect
from oauth2client import client, crypt
from app import app, db
from forms import NewItemForm
from flask_wtf.csrf import CsrfProtect
from models import Item
from hashlib import md5
import os
from models import Category, Item

MY_CLIENT_ID='969890289717-96158do2n0gntojond0bnrmor86gdriu.apps.googleusercontent.com'
UPLOAD_FOLDER='./static/images'
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG'])


@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories)


@app.route('/oauth_check', methods=['POST'])
def oauth_check():
    token = request.get_json()['token']
    idinfo = client.verify_id_token(token, MY_CLIENT_ID)
    if idinfo['aud'] != MY_CLIENT_ID:
        return ('Wrong "client id"', 403)
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return ('Wrong issuer', 403)
    return ('ok', 200)


@app.route('/category/<int:id>/items')
def list_items(id):
    items = Item.query.filter_by(category_id = id).all()
    return render_template('items.html', items=items, category_id = id);


@app.route('/category/<int:id>/items/new')
def new_item(id):
    form = NewItemForm()
    print(form.errors)
    return render_template('new_item.html', category_id = id, form=form)


@app.route('/category/<int:id>/items/create', methods=['POST'])
def create_item(id):
    form = NewItemForm()
    if form.validate_on_submit():
        new_item = Item(name = form.data["name"], category_id = id)
        db.session.add(new_item)
        db.session.commit()
        return "ok"
    print(form.name.errors)
    return render_template('new_item.html', category_id = id, form=form)


def get_image_extension(filename):
    """ Returns the file extension if the extension is allowed, otherwise None """
    if '.' in filename:
        extension=filename.rsplit('.', 1)[1]
        if extension:
            return extension
    return None


@app.route('/upload_image', methods=['POST', 'GET'])
def upload_image():
    form = NewItemForm()
    if request.method == 'POST':
        file = request.files['file']
        if file:
            extension = get_image_extension(file.filename)
            # Save image using it's hash as filename, so two uploads with the
            # same name don't clash with each other
            if extension:
                md5_hash = md5(file.read()).hexdigest()
                filename = md5_hash + '.' + extension
                savepath=os.path.join(UPLOAD_FOLDER, filename)
                file.seek(0)
                file.save(savepath)
                return '''Success'''
    return render_template('upload_image.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

