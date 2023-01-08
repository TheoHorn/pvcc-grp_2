from flask import request
from flask_login import login_required

from . import app


@app.get('/handle_garden')
@login_required
def your_garden():

    from jardiquest.model.path.handle_garden_model import print_garden
    return print_garden()


@app.post('/handle_garden')
@login_required
def post_garden():
    # handle case with put or delete methods
    methods = request.form.get('_method')
    from jardiquest.model.path.handle_garden_model import handle_garden_handler_model
    return handle_garden_handler_model(methods)

