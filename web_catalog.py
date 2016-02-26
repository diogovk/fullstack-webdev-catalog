#!/usr/bin/python2

from flask_wtf import Form
from flask import request, render_template, session, url_for, jsonify, Response
from app import app, db, flow
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
                           flow=flow,
                           username=session.get('username'),
                           csrf_form=Form())


@app.route('/disconnect')
def disconnect():
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
    # get short-lived token from request
    token = request.form["token"]
    return oauth.facebook_oauth(token, session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    token = request.form["token"]
    return oauth.google_oauth(token, session)


@app.route('/category/<int:id>/items')
def list_items(id):
    items = Item.query.filter_by(category_id=id).all()
    return render_template('items.html',
                           items=items,
                           category_id=id,
                           loggedin=bool(session.get('username')))


@app.route('/items/latest')
def latest_items():
    items = Item.query.order_by(Item.id.desc()).limit(9).all()
    return render_template('latest_items.html', items=items)


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


@app.route('/item/<int:id>/json', methods=['GET'])
def item_json(id):
    item = Item.query.filter_by(id=id).first()
    if item:
        return jsonify(item=item.serialize_verbose)
    resp = jsonify(error="Not found")
    resp.status_code = 404
    return resp


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


@app.route('/catalog.xml')
def catalog_xml():
    categories = Category.query.all()
    category_list = [category.serialize for category in categories]
    xml = dicttoxml(category_list, custom_root="categories")
    return Response(xml, mimetype='text/xml')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
