apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy python-bs4
apt-get -qqy install python-pip
pip2 install Flask
pip2 install oauth2client
pip2 install requests
pip2 install Flask-Migrate
pip2 install dicttoxml
pip2 install flask-wtf
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb webcatalog'
cd /vagrant
su vagrant -c 'python2 migrator.py db upgrade'
su vagrant -c 'python2 seed_database.py'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m\npython2 web_catalog.py to start the server"
echo -e $vagrantTip > /etc/motd

