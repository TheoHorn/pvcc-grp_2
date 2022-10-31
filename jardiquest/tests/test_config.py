import pytest

from jardiquest.model.database.database_handler import get_db
from jardiquest.model.database.query_builder import QueryBuilder
from jardiquest.setup_flask import create_app


# TODO test to rewrite once the content is create
# The test here are just to make sur the project is setup for the use of pytest
# And to serve as example
def test_get_db():
    flask_app = create_app()
    with flask_app.test_client():
        with flask_app.app_context():

            assert get_db() is not None
            data = QueryBuilder("SELECT * FROM test")
            data = data.fetch_all()
            assert data == [(1,), (2,), (3,)]

def test_request():
    flask_app = create_app()
    with flask_app.test_client():
        with flask_app.app_context():
            assert 1 == 1