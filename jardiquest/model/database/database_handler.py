from flask import g
import sqlite3

# path of the sqlite file
DATABASE = 'jardiquest/jardiquest.db'


# close the connection to the database call when the flask server is teardown
def close_connection(exception) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# get the connection to the database
def get_db() -> (any or None):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

