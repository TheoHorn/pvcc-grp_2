from flask import redirect, url_for, render_template, session, abort
from flask_login import current_user
from jardiquest.setup_sql import db
from sqlalchemy.sql import select, column, func
from jardiquest.model.database.entity.catalogue import Catalogue
from jardiquest.model.database.entity.recolte import Recolte

def display_market():
    garden = current_user.jardin
    if garden is None:
        return redirect(url_for('controller.garden'))
    
    produits = db.session.query(func.min(Recolte.cost).label("cheaper_price"), func.sum(Recolte.quantity).label("quantity"), Catalogue.name, Catalogue.type).join(Catalogue).group_by(Catalogue.name).filter(Recolte.idJardin == garden.idJardin).all()
    return render_template('market.html', produits=produits, garden=garden)

def display_market_product(product):
    garden = current_user.jardin
    if garden is None:
        return redirect(url_for('controller.garden'))

    product_infos = db.session.query(Catalogue).filter(Catalogue.name == product).first()
    if product_infos is None:
        abort(404)
    selling_products = db.session.query(Recolte).filter(Recolte.idJardin == garden.idJardin, Recolte.idCatalogue == product_infos.idCatalogue).all()
    return render_template('market_product.html', product=product_infos, sellings=selling_products, garden=garden, user=current_user)


def test_dataset():
    """TODO DELETE THIS FUNCTION"""
    garden = current_user.jardin
    return ""