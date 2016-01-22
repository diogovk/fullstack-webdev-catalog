import web_catalog
import unittest

class WebCatalogCase(unittest.TestCase):

    def setUp(self):
        web_catalog.app.config['TESTING'] = True
        self.app = web_catalog.app.test_client()

    def login(self, session):
        session['credentials'] = 'thisismyaccesstoken'
        session['gplus_id'] = 66666666
        session['username'] = 'John Doe'
        session['email'] = 'johndoe@example.com'
        session['provider'] = 'google'

    def test_login_button(self):
        rv = self.app.get("/")
        assert 'Login' in rv.data
        assert 'Logout' not in rv.data
        with self.app.session_transaction() as sess:
            self.login(sess)
        rv = self.app.get("/")
        assert 'Login' not in rv.data
        assert 'Logout' in rv.data

if __name__ == '__main__':
    unittest.main()

