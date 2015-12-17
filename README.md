
## Initilizing database

```
# Create the database in postgresql
createdb webcatalog

python2 migrator.py db init
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

### References
https://developers.google.com/identity/sign-in/web/backend-auth
http://flask.pocoo.org/docs/0.10/api/
http://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
https://flask-migrate.readthedocs.org/en/latest/
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
