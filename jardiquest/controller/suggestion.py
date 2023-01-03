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

    solde = current_user.balance # argent que dispose le client
    panier = glouton_solution(recoltes,solde) # lots de produits recommandés
    prix = prixPanier(panier) # prix total

    result = dict((i[3], [panier.count(i),i]) for i in panier) # dictionnaire {id_produit,[qtt,lot]}

    produits, numbs, recoltes, ids = [],[],[],[]
    
    for cle, valeur in result.items(): # création tableaux pour template
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
    ids=ids.replace("'","")
    ids=ids.replace(" ","")
    ids=ids.replace("[","")
    ids=ids.replace("]","")
    ids = ids.split(',')
    numbs = json.loads(numbs)
    for i in range(0,len(numbs)):
        selling = db.session.query(Recolte).filter(Recolte.idRecolte == ids[i]).first()
        buy_product(numbs[i]*selling.qtt_recommandee,selling)
    return redirect(url_for('controller.suggestion'))

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

def prixPanier(panier):
    somme = 0
    for i in range(0,len(panier)):
        somme = somme + panier[i][1]
    return somme
    
def glouton_solution(recoltes,solde) :
    tab = []

    for i in range(0,len(recoltes[:])): # création de lots en fonction de la quantité recommandée
        for j in range(0,int(recoltes[i].quantity/recoltes[i].qtt_recommandee)):
            tab.append([recoltes[i].idCatalogue,recoltes[i].cost*recoltes[i].qtt_recommandee,recoltes[i].qtt_recommandee,recoltes[i].idRecolte])

    tri_bulle(tab) # tri des lots en fonction du prix pour minimiser le prix du panier final
    ordre = triLoop(tab,[]) # tri pour maximiser la diversité
    
    panier = []
    for i in range(0,len(ordre)): # création du panier selon la limite du solde
        if(solde-ordre[i][1]>0):
            solde = solde - ordre[i][1]
            panier.append(ordre[i])
    return panier

def tri_bulle(tab): # tri a bulle
    n = len(tab)
    for i in range(n):
        for j in range(0, n-i-1):
            if tab[j][1] > tab[j+1][1] :
                tab[j], tab[j+1] = tab[j+1], tab[j]

def triLoop(tab,last): # tri récursif des lots afin de maximiser la diversité
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