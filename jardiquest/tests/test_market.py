from jardiquest.model.path.auth_model import *
import html5lib

html5parser = html5lib.HTMLParser(strict=True)
# file of test for the market


# make sur the path are good
def test_market_controller(test_client):
    response = test_client.get('/market')
    assert response.status_code == 200

    response = test_client.get('/market/Abricot')
    assert response.status_code == 200

    response = test_client.get('/market/catalogue')
    assert response.status_code == 200

    response = test_client.get('/market/catalogue/Abricot')
    assert response.status_code == 200

    response = test_client.get('/market/orders')
    assert response.status_code == 200


def test_auth_model(test_client):
    # test html is valid
    assert html5parser.parse(signup_model())
    assert html5parser.parse(login_model())

    assert logout_model().status_code == 302
