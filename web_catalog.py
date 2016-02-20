#!/usr/bin/python2

from flask_wtf import Form
from flask import request, render_template, redirect, session, url_for, jsonify
from oauth2client import client, crypt
from app import app, db, flow
from forms import NewItemForm
from flask_wtf.csrf import CsrfProtect
from models import Item
from models import Category, Item
from helpers import get_image_extension, save_image
import json
import requests
import urlparse


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
        if session['provider'] == 'google':
            del session['credentials']
            del session['gplus_id']
        if session['provider'] == 'facebook':
            del session['facebook_id']
        del session['username']
        del session['email']
        del session['provider']
    return ("ok", 200)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if 'provider' in session:
        return ("you're already logged in", 200)
    with open('fb_client_secret_webcatalog.json') as json_file:
        json_data = json.load(json_file)
        app_secret = json_data["app_secret"]
        app_id = json_data["app_id"]
    # get short-lived token from request
    token = request.form["token"]
    params = {
            'client_id': app_id,
            'client_secret': app_secret,
            'fb_exchange_token': token,
            'grant_type': 'fb_exchange_token'
            }
    # Get long-lived access token from facebook
    token_exchange_url = "https://graph.facebook.com/oauth/access_token"
    answer = requests.get(token_exchange_url, params=params)
    access_token = urlparse.parse_qs(answer.text)["access_token"][0]
    params = {
            'access_token': access_token,
            'fields': 'name,id,email'
            }
    api_url = 'https://graph.facebook.com/v2.4/me'
    answer = requests.get(api_url, params=params)
    data = answer.json()
    session['provider'] = 'facebook'
    session['username'] = data['name']
    session['email'] = data['email']
    session['facebook_id'] = data["id"]
    return ("ok", 200)


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
    answer = requests.get(url)
    result = answer.json()
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
    return render_template('items.html',
                           items=items,
                           category_id=id,
                           loggedin=bool(session.get('username')))


@app.route('/category/<int:id>/items/new')
def new_item(id):
    form = NewItemForm()
    form.category_id.data = id
    return render_template('edit_item.html', form=form, action="/items")


@app.route('/items', methods=['POST'])
def create_item():
    if not session.get('username'):
        return ("You must be logged in to be able to create items", 401)
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
    return render_template('show_item.html',
                           item=item,
                           username=session.get('username'),
                           csrf_form=Form())


@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    if not session.get('username'):
        return ("You must be logged in to be able to delete items", 401)
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
    if not session.get('username'):
        return ("You must be logged in to be able to delete items", 401)
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


@app.route('/catalog.json')
def catalog_json():
    categories = Category.query.all()
    category_list = [category.serialize for category in categories]
    return jsonify(categories=category_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
