#!/usr/bin/python2

from flask import Flask

app = Flask(__name__)

@app.route('/')
def login_page():
    return app.send_static_file('google_sign_in.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

