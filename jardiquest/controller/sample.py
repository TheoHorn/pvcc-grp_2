from flask import render_template
from . import app


@app.get('/')
def test():
    return render_template('sample.html')
