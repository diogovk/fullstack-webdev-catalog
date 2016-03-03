
## Dependencies

To install dependencies in a apt based sistem:
```
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy python-bs4
apt-get -qqy install python-pip
pip2 install Flask
pip2 install oauth2client
pip2 install requests
pip2 install Flask-Migrate
pip2 install dicttoxml
pip2 install flask-wtf
```

## Quickstart

To setup a virtual machine using vagrant and run the web application:
```
vagrant up
vagrant ssh
# inside ssh
cd /vagrant
./web_catalog.py
```

Then access the web application running in http://localhost:5000

## WebApp credentials with Google

For google oauth login, it is nececessary to have a credential with google for your app.
To do that, you'll have to create a project in https://console.developers.google.com/project (if you don't have already).
And then, create credentials in https://console.developers.google.com/apis/credentials?project=<YOUR_PROJECT>.
Then, in the same page, download the JSON file with your credentials.
Save the downloaded file in client_secret_webcatalog.json at the webapp root directory (which contains this README).
Remember that the credentials in your JSON file are secret, and should NOT be commited in a public project!
This project comes with a sample google credential, which shouldn't be used in production.

## WebApp credentials with Facebook

As with google oauth, you need credentials with facebook for proper facebook 
login funcionality.
Those credentials are read from the file fb_client_secret_webcatalog.json.


## Initilizing database

```
# Set up database structure in postgres
createdb webcatalog
python2 migrator.py db upgrade
```

## Create DB migratons after changing models

After changing models (classes extending db.Model) you can create a migration
automatically and apply to the database with the following:

```
python2 migrator.py db migrate
# Check the migration file, and when finished:
python2 migrator.py db upgrade
```

## Populate the database with seed data

This project comes with example data that can be inserted in the database for
easier demonstration.
```
python2 seed_database.py
```

## Starting the webapp

To start the web application, execute:
```
./web-catalog.py
```

You'll be able to access it in http://localhost:5000/

## CRUD: Edit/Delete

Please note that you'll only be able to delete edit items that were created with your user.
Items inserted from seed data, are associated with the seed user "seeduser@example.com" and 
won't be changeable from the web interface until associated with a user that can actually login.

This can be done using the following, directly in the database:
```
update "user" set email='youremail@gmail.com' where email='seeduser@example.com';
```


## Execute tests
```
python2 tests.py
```

## Check JSON and XML endpoints
```
# Headers
curl -I http://localhost:5000/catalog.json
curl -I http://localhost:5000/catalog.xml
# Content
curl http://localhost:5000/catalog.json
curl http://localhost:5000/catalog.xml
# Get specific item
curl http://localhost:5000/item/9/json
```


### References
https://developers.google.com/identity/sign-in/web/backend-auth
http://flask.pocoo.org/docs/0.10/api/
http://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
https://flask-migrate.readthedocs.org/en/latest/
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
http://stackoverflow.com/questions/7428124/how-can-i-fake-request-post-and-get-params-for-unit-testing-in-flask
http://stackoverflow.com/questions/8552675/form-sending-error-flask
https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUpClass
