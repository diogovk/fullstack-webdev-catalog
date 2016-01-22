import web_catalog
import unittest

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

if __name__ == '__main__':
    unittest.main()

