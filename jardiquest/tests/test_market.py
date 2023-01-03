from jardiquest.setup_flask import create_app
from jardiquest.model.path.market_model import *
import html5lib
import unittest

html5parser = html5lib.HTMLParser(strict=True)
# file of test for the market

#test_client.post('/login', data={'email': 'a@gmail.com', 'password' : 'azertyui'})

user1 = {'username': 'a', 'email': 'a@gmail.com', 'password': 'azertyui'}
user2 = {'username': 'b', 'email': 'b@gmail.com', 'password': 'azertyui'}
class TestUserLogged(unittest.TestCase):
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email = email,
            password=password
        ), follow_redirects=True)

    def setUp(self):
        app = create_app()
        db.app = app  #
        self.app = app.test_client()
        self.login("a@gmail.com", "azertyui")

    def tearDown(self):
        pass

    def register_user(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
        ), follow_redirects=True)


    def test_login(self):
        resp = self.login(user1.get('email'), user1.get('password'))
        assert resp.status_code == 200

    def test_market(self):
        assert(False)
    

class TestUserNotLogged(unittest.TestCase):
    def setUp(self):
        app = create_app()
        db.app = app  
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_catalogue(self):
        resp = self.app.get('/market')
        assert(resp.status_code == 302)

    

    def test_get_sell_product(self):
        resp = self.app.get('/market/catalogue')
        assert(resp.status_code == 302)
    
    def test_get_market(self):
        resp = self.app.get('/market')
        assert(resp.status_code == 302)
        