import web_catalog
import unittest
from app import db
from models import Item, Category
from bs4 import BeautifulSoup
import json


def get_existing_category_id():
    return Category.query.first().id


class WebCatalogCase(unittest.TestCase):

    def setUp(self):
        web_catalog.app.config['TESTING'] = True
        self.app = web_catalog.app.test_client()

    def login(self):
        """ Mock login, as to avoid hitting google auth servers in tests """
        with self.app.session_transaction() as sess:
            sess['access_token'] = 'thisismyaccesstoken'
            sess['gplus_id'] = 66666666
            sess['username'] = 'John Doe'
            sess['email'] = 'johndoe@example.com'
            sess['provider'] = 'google'

    def logout(self):
        """ Logs out from the app returning server response"""
        return self.app.get("/disconnect")

    def get_crsf_token_from_url(self, url):
        """ GET the url, parsing the response and returns the crsf_token """
        page = self.app.get(url).data
        soup = BeautifulSoup(page, "html.parser")
        crsf_input = soup.find("input", id="csrf_token")
        return crsf_input.get('value')

    def test_login_button(self):
        """
        Login button should appear when logged off, but not when logged in.
        Logout button should appear when logged in, but not when logged off.
        """
        rv = self.app.get("/")
        assert 'Login' in rv.data
        assert 'Logout' not in rv.data
        self.login()
        rv = self.app.get("/")
        assert 'Login' not in rv.data
        assert 'Logout' in rv.data
        rv = self.logout()
        assert rv.data == "ok"
        rv = self.app.get("/")
        assert 'Login' in rv.data
        assert 'Logout' not in rv.data

    def test_csrf_check(self):
        '''
        Should reject the request if POST if doesn't have a valid crsf_token
        '''
        item_count = db.session.query(Item.id).count()
        category_id = get_existing_category_id()
        self.login()
        rv = self.app.post("/items", data=dict(
            name="Thingy", description="A Thingy thing",
            category_id=category_id,
            csrf_token="thisisaninvalidcrfstoken"))
        assert rv.status_code == 400
        rv = self.app.post("/items", data=dict(
            name="Thingy", description="A Thingy thing",
            category_id=category_id))
        assert rv.status_code == 400
        current_item_count = db.session.query(Item.id).count()
        assert item_count == current_item_count
        self.logout()

    def test_new_item(self):
        item_count = db.session.query(Item.id).count()
        category_id = get_existing_category_id()
        self.login()
        # should accept and add to the DB if crsf_token is correct
        csrf_token = self.get_crsf_token_from_url(
                "/category/%s/items/new" % category_id)
        rv = self.app.post("/items", data=dict(
            name="Thingy",
            description="A Thingy thing",
            category_id=category_id,
            csrf_token=csrf_token))
        assert rv.status_code == 200
        assert rv.data == "ok"
        current_item_count = db.session.query(Item.id).count()
        assert (item_count+1) == current_item_count
        self.logout()

    def test_edit_item(self):
        self.login()
        item = db.session.query(Item).filter_by(name="Thingy").first()
        csrf_token = self.get_crsf_token_from_url("%s/edit" % item.url)
        rv = self.app.post(item.url, data=dict(
            name="Renamed Thingy",
            description="A Thingy thing",
            csrf_token=csrf_token))
        assert rv.status_code == 200
        assert rv.data == "ok"
        updated_item = db.session.query(Item).filter_by(id=item.id).first()
        assert updated_item.name == "Renamed Thingy"
        self.logout()

    def test_delete_item(self):
        item_count = db.session.query(Item.id).count()
        self.login()
        item = db.session.query(Item).filter_by(name="Renamed Thingy").first()
        csrf_token = self.get_crsf_token_from_url("%s" % item.url)
        rv = self.app.delete(item.url, data=dict(csrf_token=csrf_token))
        assert rv.status_code == 200
        assert rv.data == "ok"
        current_item_count = db.session.query(Item.id).count()
        assert (item_count-1) == current_item_count
        self.logout()


    def test_category_json(self):
        rv = self.app.get("/catalog.json")
        assert rv.status_code == 200
        # Will raise exception if not valid JSON
        json.loads(rv.data)


if __name__ == '__main__':
    unittest.main()
