#!/usr/bin/python2

from flask_wtf import Form
from flask import request, render_template, redirect
from oauth2client import client, crypt
from app import app, db
from forms import NewItemForm
from flask_wtf.csrf import CsrfProtect
from models import Item
from models import Category, Item
from helpers import get_image_extension, save_image

MY_CLIENT_ID='969890289717-96158do2n0gntojond0bnrmor86gdriu.apps.googleusercontent.com'


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
    action = "/category/%s/items" % id
    return render_template('edit_item.html', form = form, action = action)


@app.route('/category/<int:id>/items', methods=['POST'])
def create_item(id):
    form = NewItemForm()
    if form.validate_on_submit():
        file = request.files[form.image_file.name]
        saved_path = save_image(file)
        new_item = Item(name = form.data["name"],
                category_id = id,
                description = form.data["description"],
                image_file = saved_path)
        db.session.add(new_item)
        db.session.commit()
        return "ok"
    action = "/category/%s/items" % id
    return render_template('edit_item.html', form = form, action = action)


@app.route('/item/<int:id>', methods=['GET'])
def show_item(id):
    item = Item.query.filter_by(id = id).first()
    csrf_form = Form()
    return render_template('show_item.html', item = item, csrf_form = csrf_form)


@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.filter_by(id = id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return "ok"
    return "Not Found", 404


@app.route('/item/<int:id>/edit')
def edit_item(id):
    item = Item.query.filter_by(id = id).first()
    if item:
        form = NewItemForm(obj=item)
        action = "/item/%s" % item.id
        return render_template('edit_item.html', form = form, action = action)
    return "Not Found", 404


@app.route('/item/<int:id>', methods=['PUT', 'POST'])
def update_item(id):
    item = Item.query.filter_by(id = id).first()
    if not item:
        return "Not Found", 404
    form = NewItemForm(obj=item)
    if form.validate_on_submit():
        file = request.files[form.image_file.name]
        saved_path = save_image(file)
        if saved_path:
            item.image_file = saved_path
        item.name = form.data["name"]
        item.description = form.data["description"]
        db.session.commit()
        return "ok"
    action = "/item/%s" % item.id
    return render_template('edit_item.html', form = form, action = action)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

