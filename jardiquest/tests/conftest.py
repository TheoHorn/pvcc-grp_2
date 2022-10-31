import pytest

from jardiquest.setup_flask import create_app


# Allow to not write the lines in the test_function everywhere but instead just pass testing_client in argument
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
