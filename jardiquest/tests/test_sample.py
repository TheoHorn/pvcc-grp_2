from jardiquest.model.database.sql.database_handler import get_db
from jardiquest.model.database.sql.query_builder import QueryBuilder


# TODO should change once the program is well avance (their not guaranteed to work everytime)
# The test here are just to make sur the project is setup for the use of pytest
# And to serve as example


# example how to use the database
def test_get_db(test_client):
    assert get_db() is not None
    data = QueryBuilder("SELECT * FROM user")
    data.fetch_all()


# example of how to make query to the server in the test function
def test_request(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
