import web_catalog
import unittest
from app import db
from models import Item, Category
from bs4 import BeautifulSoup


def get_existing_category_id():
    return Category.query.first().id


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

    def get_crsf_token_from_url(self, url):
        page = self.app.get(url).data
        soup = BeautifulSoup(page, "html.parser")
        crsf_input = soup.find("input", id="csrf_token")
        return crsf_input.get('value')

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

    def test_csrf_check(self):
        item_count = db.session.query(Item.id).count()
        category_id = get_existing_category_id()
        create_item_url = "/category/%s/items" % category_id
        # should reject if post if doesn't have crsf_token
        rv = self.app.post(create_item_url, data=dict(
            name="Thingy", description="A Thingy thing"))
        assert rv.status_code == 400
        current_item_count = db.session.query(Item.id).count()
        assert item_count == current_item_count  # no increase

    def test_new_item(self):
        item_count = db.session.query(Item.id).count()
        category_id = get_existing_category_id()
        create_item_url = "/category/%s/items" % category_id
        # should accept and add to the DB if crsf_token is correct
        csrf_token = self.get_crsf_token_from_url(
                "/category/%s/items/new" % category_id)
        rv = self.app.post(create_item_url, data=dict(
            name="Thingy",
            description="A Thingy thing",
            csrf_token=csrf_token))
        assert rv.status_code == 200
        current_item_count = db.session.query(Item.id).count()
        assert (item_count+1) == current_item_count

    def test_edit_item(self):
        item = db.session.query(Item).filter_by(name="Thingy").first()
        csrf_token = self.get_crsf_token_from_url("%s/edit" % item.url)
        rv = self.app.post(item.url, data=dict(
            name="Renamed Thingy",
            description="A Thingy thing",
            csrf_token=csrf_token))
        assert rv.status_code == 200
        updated_item = db.session.query(Item).filter_by(id=item.id).first()
        assert updated_item.name == "Renamed Thingy"


if __name__ == '__main__':
    unittest.main()
