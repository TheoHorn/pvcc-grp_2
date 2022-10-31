from flask import render_template
from . import app
from ..model.database.query_builder import QueryBuilder


@app.get('/')
def test():
    data = QueryBuilder("SELECT * FROM test")
    data = data.fetch_all()
    return render_template('test.html', datas=data)
