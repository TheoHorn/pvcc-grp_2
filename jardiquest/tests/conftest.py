import pytest
from jardiquest.setup_sql import db
from jardiquest.setup_flask import create_app


# Allow to not write the lines in the test_function everywhere but instead just pass testing_client in argument
@pytest.fixture(scope='module')
def app():
    flask_app = create_app()
    with flask_app.test_client() as app:
        with flask_app.app_context():
            yield app

@pytest.fixture(scope='class')
def db(app):
    f = open('jardiquest/tests/dataset/dataset.sqlite')
    db.create_all()
    for l in f.readlines():
        print(l)
        db.session.connection().execute(l)
        db.session.commit()
    f.close()
    yield db
    db.drop_all()
