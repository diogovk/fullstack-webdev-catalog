#!/usr/bin/python2

from flask_wtf import Form
from flask import request, render_template, redirect, session, url_for
from oauth2client import client, crypt
from app import app, db, flow
from forms import NewItemForm
from flask_wtf.csrf import CsrfProtect
from models import Item
from models import Category, Item
from helpers import get_image_extension, save_image
import httplib2
import json
import requests


@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories,
                           flow=flow,
                           username=session.get('username'),
                           csrf_form=Form())

@app.route('/disconnect')
def disconnect():
    if 'provider' in session:
        del session['credentials']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['provider']
    return redirect(url_for('home'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    token = request.form["token"]
    try:
        credentials = flow.step2_exchange(token)
    except FlowAExchangeError:
        return ('Failed to upgrade the authorization token (step2)', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        return (result.get('error'), 500)

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return ("Token's used ID doesn't match given user", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != flow.client_id:
        return ("Token's client ID does not match app's", 401)

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return ('Current user is already connected', 200)

    session['credentials'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    session['username'] = data['name']
    session['email'] = data['email']
    session['provider'] = 'google'
    return ('ok', 200)


@app.route('/category/<int:id>/items')
def list_items(id):
    items = Item.query.filter_by(category_id=id).all()
    return render_template('items.html', items=items, category_id=id)


@app.route('/category/<int:id>/items/new')
def new_item(id):
    form = NewItemForm()
    form.category_id.data = id
    return render_template('edit_item.html', form=form, action="/items")


@app.route('/items', methods=['POST'])
def create_item():
    form = NewItemForm()
    if form.validate_on_submit():
        file = request.files.get(form.image_file.name)
        saved_path = save_image(file) if file else None
        new_item = Item(name=form.data["name"],
                        category_id=form.data["category_id"],
                        description=form.data["description"],
                        image_file=saved_path)
        db.session.add(new_item)
        db.session.commit()
        return "ok"
    return render_template('edit_item.html', form=form, action="/items")


@app.route('/item/<int:id>', methods=['GET'])
def show_item(id):
    item = Item.query.filter_by(id=id).first()
    # CSRF needed for delete function
    return render_template('show_item.html', item=item, csrf_form=Form())


@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return "ok"
    return "Not Found", 404


@app.route('/item/<int:id>/edit')
def edit_item(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        form = NewItemForm(obj=item)
        return render_template('edit_item.html', form=form, action=item.url)
    return "Not Found", 404


@app.route('/item/<int:id>', methods=['PUT', 'POST'])
def update_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Not Found", 404
    form = NewItemForm(obj=item)
    if form.validate_on_submit():
        file = request.files.get(form.image_file.name)
        saved_path = save_image(file) if file else None
        if saved_path:
            item.image_file = saved_path
        item.name = form.data["name"]
        item.description = form.data["description"]
        db.session.commit()
        return "ok"
    return render_template('edit_item.html', form=form, action=item.url)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
