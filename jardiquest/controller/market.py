from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_required
from . import app

@app.get('/market')
@login_required
def market():
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_market
        return display_market()
    else:
        return redirect(url_for('login'))


@app.get('/market/<string:product>')
@login_required
def market_product(product):
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_market_product
        return display_market_product(product)
    else:
        return redirect(url_for('login'))


@app.get('/test_dataset')
def test_dataset():
    """TODO DELETE THIS FUNCTION"""
    from jardiquest.model.path.market_model import test_dataset
    return test_dataset()