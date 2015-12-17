#!/usr/bin/python2

from flask import request, render_template
from oauth2client import client, crypt
from app import app, db

MY_CLIENT_ID='969890289717-96158do2n0gntojond0bnrmor86gdriu.apps.googleusercontent.com'

from models import Category

@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories)
    return app.send_static_file('google_sign_in.html')

@app.route('/oauth_check', methods=['POST'])
def oauth_check():
    token = request.get_json()['token']
    idinfo = client.verify_id_token(token, MY_CLIENT_ID)
    if idinfo['aud'] != MY_CLIENT_ID:
        return ('Wrong "client id"', 403)
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return ('Wrong issuer', 403)
    return ('ok', 200)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

