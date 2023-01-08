from jardiquest.model.path.auth_model import *
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
    assert response.status_code == 405
