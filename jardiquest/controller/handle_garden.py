from flask import request
from flask_login import login_required

from . import app


@app.get('/handle_garden')
@login_required
def all_garden():

    from jardiquest.model.path.handle_garden_model import print_garden
    return print_garden()

