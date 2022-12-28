from flask import redirect, url_for, session, request
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


@app.post('/market/<string:product>/buy')
@login_required
def market_buy(product):
    # TODO Récupérer quantité et prix
    quantity = float(request.form['buy_quantity'])
    selling_id = request.form['selling_id']
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import market_buy
        return market_buy(quantity, selling_id)
    else:
        return redirect(url_for('login'))