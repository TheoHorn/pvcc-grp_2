from jardiquest.model.path.auth_model import *
import html5lib

html5parser = html5lib.HTMLParser(strict=True)

# make sur the path are good
def test_auth_controller(test_client):
    response = test_client.get('/garden')
    assert response.status_code == 200

    response = test_client.get('/new')
    assert response.status_code == 200

    response = test_client.get('/modify')
    assert response.status_code == 200