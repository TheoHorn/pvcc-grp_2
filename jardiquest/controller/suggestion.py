from flask import render_template
from flask_login import current_user, login_required
from jardiquest.controller import app
from jardiquest.setup_sql import db
from flask import *
from flask_login import *
from . import app
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.annonce import Annonce
from jardiquest.model.database.entity.recolte import Recolte
from jardiquest.model.database.entity.catalogue import Catalogue
from jardiquest.model.database.entity.commande import Commande
import math
import uuid
from datetime import datetime

@app.route('/suggestion')
@login_required
def suggestion():    
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if jardin is not None :
        recoltes = Recolte.query.filter(Recolte.idJardin == jardin.idJardin)
    else :
        recoltes = []

    solde = current_user.balance # money the customer has
    if solde==None : solde = 0

    panier = glouton_solution(recoltes,solde) # recommended product bundles
    prix = prixPanier(panier) # total price

    result = creation_dictionnaire(panier) # dictionary {id_produit,[qtt,lot]}

    produits, numbs, recoltes, ids = [],[],[],[]
    
    for cle, valeur in result.items(): # creating tables for template
        catalogue = Catalogue.query.filter(Catalogue.idCatalogue == valeur[1][0]).first()
        recolte = Recolte.query.filter(Recolte.idRecolte == cle).first()
        produits.append(catalogue)
        recoltes.append(recolte)
        numbs.append(valeur[0])
        ids.append(cle)

    return render_template('suggestion.html',jardin = jardin,user = current_user,recoltes = recoltes,numbs = numbs,produits = produits,prix = prix, length = len(result), ids = ids)

@app.route('/buy/<numbs>/<ids>')
@login_required
def buy(numbs,ids):
    try:
        ids = jsonify(ids)
        numbs = json.loads(numbs)
    except:
        ids = []
        numbs = []
    for i in range(0,len(numbs)):
        selling = db.session.query(Recolte).filter(Recolte.idRecolte == ids[i]).first()
        if(selling.qtt_recommandee is not None):
            buy_product(numbs[i]*selling.qtt_recommandee,selling)
    return redirect(url_for('controller.suggestion'))

def jsonify(ids):
    ids=ids.replace("'","")
    ids=ids.replace(" ","")
    ids=ids.replace("[","")
    ids=ids.replace("]","")
    return ids.split(',')

def buy_product(quantity,selling):
    if selling is None or quantity > selling.quantity or quantity <= 0 or selling.jardin != current_user.jardin:
        abort(404)

    totalPrice = selling.cost * quantity

    if current_user.balance < totalPrice:
        flash("Votre solde n'est pas suffisant", "error")
    else:
        # If no error : 
        # Decrease quantity, and delete if no more
        selling.quantity -= quantity
        selling.quantity = math.floor(selling.quantity*100)/100
    
        # Decrease user balance
        current_user.balance -= totalPrice
        current_user.balance = math.floor(current_user.balance*100)/100

        # Create an order
        commande = Commande(idCommande = uuid.uuid1().hex, acheteur=current_user.email, idRecolte=selling.idRecolte, quantite=quantity, cout = totalPrice , dateAchat = datetime.now())
        db.session.add(commande)
        db.session.commit()

def creation_dictionnaire(panier):
    return dict((i[3], [panier.count(i),i]) for i in panier)

def prixPanier(panier):
    somme = 0
    for i in range(0,len(panier)):
        somme = somme + panier[i][1]
    return somme
    
def glouton_solution(recoltes,solde) :

    tab = creation_lots(recoltes) # First step : creation of batches according to the recommended quantity
    
    tri_bulle(tab) # Second step : sorting lots by price to minimize the final basket price
    
    ordre = triLoop(tab,[]) # Third step : sorting to maximize diversity

    panier = remplir_panier(ordre,solde) # Fourth step :creation of the basket according to the limit of the balance

    return panier

def creation_lots(recoltes):
    tab = []
    for i in range(0,len(recoltes[:])):
        if(recoltes[i].cost!=None and recoltes[i].quantity!=None and recoltes[i].qtt_recommandee != None and recoltes[i].idCatalogue!=None and recoltes[i].idRecolte!=None):
            for j in range(0,int(recoltes[i].quantity/recoltes[i].qtt_recommandee)):
                tab.append([recoltes[i].idCatalogue,recoltes[i].cost*recoltes[i].qtt_recommandee,recoltes[i].qtt_recommandee,recoltes[i].idRecolte])
    return tab

def remplir_panier(ordre,solde):
    panier = []
    for i in range(0,len(ordre)):
        if(solde-ordre[i][1]>0):
            solde = solde - ordre[i][1]
            panier.append(ordre[i])
    return panier

def tri_bulle(tab): # bubble sorting
    n = len(tab)
    for i in range(n):
        for j in range(0, n-i-1):
            if tab[j][1] > tab[j+1][1] :
                tab[j], tab[j+1] = tab[j+1], tab[j]

def triLoop(tab,last): # recursive sorting of batches to maximize diversity
    liste = tab[:]
    memoire = []
    panier = []
    for i in range(0,len(liste)):
        if(liste[i][0] not in memoire):
            memoire.append(liste[i][0])
            panier.append(liste[i])
            liste[i]=0
    liste = [value for value in liste if value != 0]

    if(liste!=[]):   
        return triLoop(liste,last+panier)
    else :
        return last+panier