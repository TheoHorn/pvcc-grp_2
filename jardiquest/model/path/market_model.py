from flask import redirect, url_for, render_template, session, abort
from flask_login import current_user
from jardiquest.setup_sql import db
from sqlalchemy.sql import select, column, func
import uuid
import math
from datetime import datetime
from jardiquest.model.database.entity.catalogue import Catalogue
from jardiquest.model.database.entity.recolte import Recolte
from jardiquest.model.database.entity.commande import Commande

def display_market():
    garden = current_user.jardin
    if garden is None:
        return redirect(url_for('controller.garden'))

    produits = db.session.query(func.min(Recolte.cost).label("cheaper_price"), func.sum(Recolte.quantity).label("quantity"), Catalogue.name, Catalogue.type, Catalogue.imagePath).join(Catalogue).group_by(Catalogue.name).filter(Recolte.idJardin == garden.idJardin).all()
    return render_template('market.html', produits=produits, garden=garden)

def display_market_product(product):
    garden = current_user.jardin
    if garden is None:
        return redirect(url_for('controller.garden'))

    product_infos = db.session.query(Catalogue).filter(Catalogue.name == product).first()
    if product_infos is None:
        abort(404)
    selling_products = db.session.query(Recolte).filter(Recolte.idJardin == garden.idJardin, Recolte.idCatalogue == product_infos.idCatalogue).order_by(Recolte.cost).all()
    return render_template('market_product.html', product=product_infos, sellings=selling_products, garden=garden, user=current_user)


def market_buy(quantity, selling_id):
    # TODO vérifier que quantité <= stock, vérifier que prix <= soldeUser
    #      Si ok, décrémenter stock (supprimer si = à 0), décrémenter soldeUser et créer un bon de commande non traité
    selling = db.session.query(Recolte).filter(Recolte.idRecolte == selling_id).first()
    product_name = selling.catalogue.name
    if selling is None:
        abort(404)
    if quantity > selling.quantity:
        # Error
        return "error quantity"
    totalPrice = selling.cost * quantity
    if current_user.balance < totalPrice:
        # Error
        return "error balance"
        pass
    else:
        # If no error : 
        # Decrease quantity, and delete if no more
        selling.quantity -= quantity
        selling.quantity = math.floor(selling.quantity*100)/100
        if selling.quantity < 0.05:
            db.session.delete(selling)
    
        # Decrease user balance
        current_user.balance -= totalPrice
        current_user.balance = math.floor(current_user.balance*100)/100

        # Create an order
        commande = Commande(idCommande = uuid.uuid1().hex, acheteur=current_user.email, recolte=selling_id, quantite=quantity, dateAchat = datetime.now())
        db.session.add(commande)
        db.session.commit()

        return redirect(url_for('controller.market_product', product=product_name))