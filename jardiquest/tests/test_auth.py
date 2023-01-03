from jardiquest.model.path.auth_model import *
import html5lib

html5parser = html5lib.HTMLParser(strict=True)
# file of test for the auth
# controller and model part


# make sur the path are good
def test_auth_controller(app):
    response = app.get('/login')
    assert response.status_code == 200

    response = app.get('/signup')
    assert response.status_code == 200

    response = app.post('/login')
    assert response.status_code == 302

    response = app.post('/signup')
    assert response.status_code == 302

    response = app.get('/logout')
    assert response.status_code == 302


def test_auth_model(app):
    # test html is valid
    assert html5parser.parse(signup_model())
    assert html5parser.parse(login_model())

    assert logout_model().status_code == 302
