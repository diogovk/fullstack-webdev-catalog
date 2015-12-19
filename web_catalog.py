#!/usr/bin/python2

from flask import request, render_template
from oauth2client import client, crypt
from app import app, db

MY_CLIENT_ID='969890289717-96158do2n0gntojond0bnrmor86gdriu.apps.googleusercontent.com'

from models import Category, Item

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

@app.route('/category/<id>/items', methods=['GET'])
def list_items(id):
    items = Item.query.filter_by(category_id = id).all()
    return render_template('items.html', items=items);



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

