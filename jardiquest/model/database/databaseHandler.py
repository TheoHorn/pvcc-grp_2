from flask import g
import sqlite3

DATABASE = 'jardiquest.db'


# close the connection to the database call when the flask server is teardown
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
