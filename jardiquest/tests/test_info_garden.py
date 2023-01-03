from jardiquest.model.path.auth_model import *
import html5lib

html5parser = html5lib.HTMLParser(strict=True)

# make sur the path are good
def test_auth_controller(app):
    response = app.get('/garden')
    assert response.status_code == 200

    response = app.get('/new')
    assert response.status_code == 200

    response = app.get('/modify')
    assert response.status_code == 200