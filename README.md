
## Dependencies

```
python2-flask
python2-flask-wtf
python2-psycopg2
apiclient
oauth2client
SQLAlchemy
Flask-Migrate
dicttoxml
```

## WebApp credentials with Google

For google oauth login, it is nececessary to have a credential with google.
To do that, you'll have to create a project in https://console.developers.google.com/project (if you don't have already).
And then, create credentials in https://console.developers.google.com/apis/credentials?project=<YOUR_PROJECT>.
Then, in the same page, download the JSON file with your credentials.
Save the downloaded file in client_secret_webcatalog.json at the webapp root directory (which contains this README).
Remember the credentials in your JSON file are secret, and should NOT be commited in a public project!
This project comes with a sample google credential, which shouldn't be used in production.

## Initilizing database

```
# Create the database in postgresql
createdb webcatalog

python2 migrator.py db upgrade
```

## Create DB migratons after changing models
```
python2 migrator.py db migrate
# Check the migration file, and when finished:
python2 migrator.py db upgrade
```

## Populate the database with seed data
```
python2 seed_database.py
```

## Starting the webapp
```
./web-catalog.py
```

## Execute tests
```
python2 tests.py
```

## Check JSON and XML endpoints
```
curl -I http://localhost:5000/catalog.json
curl http://localhost:5000/catalog.json
curl -I http://localhost:5000/catalog.xml
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
