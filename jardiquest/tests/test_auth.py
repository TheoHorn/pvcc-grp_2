from jardiquest.model.path.auth_model import *
import html5lib

html5parser = html5lib.HTMLParser(strict=True)
# file of test for the auth
# controller and model part


# make sur the path are good
def test_auth_controller(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200

    response = test_client.get('/signup')
    assert response.status_code == 200

    response = test_client.post('/login')
    assert response.status_code == 302

    response = test_client.post('/signup')
    assert response.status_code == 302

    response = test_client.get('/logout')
    assert response.status_code == 302


def test_auth_model(test_client):
    # test html is valid
    assert html5parser.parse(signup_model())
    assert html5parser.parse(login_model())

    assert logout_model().status_code == 302
