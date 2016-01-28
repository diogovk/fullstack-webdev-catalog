import web_catalog
import unittest
from app import db
from models import Item, Category
from bs4 import BeautifulSoup


def get_existing_category_id():
    return Category.query.first().id


def get_crsf_token(page):
    soup = BeautifulSoup(page, "html.parser")
    crsf_input = soup.find("input", id="csrf_token")
    return crsf_input.get('value')


class WebCatalogCase(unittest.TestCase):

    def setUp(self):
        web_catalog.app.config['TESTING'] = True
        self.app = web_catalog.app.test_client()

    def login(self):
        # Mock login, as to avoid hitting google auth servers in tests
        with self.app.session_transaction() as sess:
            sess['credentials'] = 'thisismyaccesstoken'
            sess['gplus_id'] = 66666666
            sess['username'] = 'John Doe'
            sess['email'] = 'johndoe@example.com'
            sess['provider'] = 'google'


    def test_login_button(self):
        rv = self.app.get("/")
        assert 'Login' in rv.data
        assert 'Logout' not in rv.data
        self.login()
        rv = self.app.get("/")
        assert 'Login' not in rv.data
        assert 'Logout' in rv.data
        rv = self.app.get("/disconnect", follow_redirects=True)
        assert 'Login' in rv.data
        assert 'Logout' not in rv.data


    def test_new_item(self):
        item_count = db.session.query(Item.id).count()
        category_id = get_existing_category_id()
        create_item_url = "/category/%s/items" % category_id
        # should reject if post if doesn't have crsf_token
        rv = self.app.post(create_item_url, data=dict(name="Thingy", description="A Thingy thing"))
        assert rv.status_code == 400
        current_item_count = db.session.query(Item.id).count()
        assert item_count == current_item_count #no increase
        # should accept and add to the DB if crsf_token is correct
        rv = self.app.get("/category/%s/items/new" % category_id)
        csrf_token = get_crsf_token(rv.data)
        rv = self.app.post(create_item_url, data=dict(name="Thingy", description="A Thingy thing", csrf_token=csrf_token))
        current_item_count = db.session.query(Item.id).count()
        assert (item_count+1) == current_item_count

if __name__ == '__main__':
    unittest.main()

