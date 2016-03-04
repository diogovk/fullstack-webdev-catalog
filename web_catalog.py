#!/usr/bin/python2

from flask_wtf import Form
from flask import request, render_template, session, url_for, jsonify, Response
from app import app, db
from forms import NewItemForm
from flask_wtf.csrf import CsrfProtect
from models import Item
from models import Category, Item
from helpers import get_image_extension, save_image
# do not confuse requests with flask.request
import oauth
from dicttoxml import dicttoxml


@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories,
                           flow=oauth.flow,
                           logged_in=(session.get('user_id') is not None),
                           csrf_form=Form())


@app.route('/disconnect')
def disconnect():
    ''' Disconnects a logged in user '''
    if 'provider' in session:
        if session['provider'] == 'google':
            oauth.google_revoke_token(session.get("access_token"))
            del session['gplus_id']
        if session['provider'] == 'facebook':
            oauth.facebook_revoke_token(
                    session.get("facebook_id"), session.get("access_token"))
            del session['facebook_id']
        del session['access_token']
        del session['username']
        del session['user_id']
        del session['email']
        del session['provider']
    return ("ok", 200)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    ''' Logs in a user using facebook oath '''
    # get short-lived token from request
    token = request.form["token"]
    return oauth.facebook_oauth(token, session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Logs in a user using google oath '''
    token = request.form["token"]
    return oauth.google_oauth(token, session)


@app.route('/category/<int:id>/items')
def list_items(id):
    ''' list items of a category in a grid  '''
    items = Item.query.filter_by(category_id=id).all()
    return render_template('items.html',
                           items=items,
                           category_id=id,
                           logged_in=(session.get('user_id') is not None))


@app.route('/items/latest')
def latest_items():
    ''' list the latest 9 saved items  '''
    items = Item.query.order_by(Item.id.desc()).limit(9).all()
    return render_template('latest_items.html', items=items)


@app.route('/category/<int:id>/items/new')
def new_item(id):
    ''' Form for creating a new Item '''
    form = NewItemForm()
    form.category_id.data = id
    return render_template('edit_item.html', form=form, action="/items")


@app.route('/items', methods=['POST'])
def create_item():
    ''' Save a new Item in the database '''
    owner_id = session.get('user_id')
    if not owner_id:
        return ("You must be logged in to be able to create items", 401)
    form = NewItemForm()
    if form.validate_on_submit():
        file = request.files.get(form.image_file.name)
        saved_path = save_image(file) if file else None
        new_item = Item(name=form.data["name"],
                        category_id=form.data["category_id"],
                        description=form.data["description"],
                        image_file=saved_path,
                        owner_id=owner_id)
        db.session.add(new_item)
        db.session.commit()
        return "ok"
    return render_template('edit_item.html', form=form, action="/items")


@app.route('/item/<int:id>/json', methods=['GET'])
def item_json(id):
    ''' JSON representation of an Item '''
    item = Item.query.filter_by(id=id).first()
    if item:
        return jsonify(item=item.serialize_verbose)
    resp = jsonify(error="Not found")
    resp.status_code = 404
    return resp


@app.route('/item/<int:id>', methods=['GET'])
def show_item(id):
    ''' Page showing Item's details such as description and image '''
    item = Item.query.filter_by(id=id).first()
    user_id = session.get('user_id')
    is_owner = user_id is not None and (user_id == item.owner_id)
    return render_template('show_item.html',
                           item=item,
                           is_owner=is_owner,
                           # CSRF needed for delete function
                           csrf_form=Form())


@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    ''' Delete an item '''
    user_id = session.get('user_id')
    if not user_id:
        return ("You must be logged in to be able to delete items", 401)
    item = Item.query.filter_by(id=id).first()
    if not item:
        return ("Not Found", 404)
    if item.owner_id != user_id:
        return ("This item doesn't belong to you", 401)
    db.session.delete(item)
    db.session.commit()
    return ("ok", 200)


@app.route('/item/<int:id>/edit')
def edit_item(id):
    ''' Get form to edit an item '''
    item = Item.query.filter_by(id=id).first()
    if item:
        form = NewItemForm(obj=item)
        return render_template('edit_item.html', form=form, action=item.url)
    return "Not Found", 404


@app.route('/item/<int:id>', methods=['PUT', 'POST'])
def update_item(id):
    ''' Updates an Item in the database '''
    user_id = session.get('user_id')
    if not user_id:
        return ("You must be logged in to be able to edit items", 401)
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Not Found", 404
    if item.owner_id != user_id:
        return ("This item doesn't belong to you", 401)
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
    ''' Get whole catalog in JSON format '''
    categories = Category.query.all()
    category_list = [category.serialize for category in categories]
    return jsonify(categories=category_list)


@app.route('/catalog.xml')
def catalog_xml():
    ''' Get whole catalog in XML format '''
    categories = Category.query.all()
    category_list = [category.serialize for category in categories]
    xml = dicttoxml(category_list, custom_root="categories")
    return Response(xml, mimetype='text/xml')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
