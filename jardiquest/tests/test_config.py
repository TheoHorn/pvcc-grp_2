from jardiquest.model.database.database_handler import get_db
from jardiquest.model.database.query_builder import QueryBuilder
from jardiquest.setup_flask import create_app


def test_get_db():
    flask_app = create_app()
    with flask_app.test_client():
        with flask_app.app_context():

            assert get_db() is not None
            data = QueryBuilder("SELECT * FROM test")
            data = data.fetch_all()
            assert data == [(1,), (2,), (3,)]
            # TODO to change because test is on specific date (just to make sur link was correct)
