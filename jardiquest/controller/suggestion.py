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

import random

@app.route('/sug')
@login_required
def suggestion():    
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if jardin is not None :
        recoltes = Recolte.query.filter(Recolte.idJardin == jardin.idJardin)
    else :
        recoltes = []

    id = []
    prix = []
    qtt_rec = []

    for i in range(0,len(recoltes[:])):
        #for j in range(0,recoltes[i].quantity):
        id.append(recoltes[i].idCatalogue)
        prix.append(recoltes[i].cost/recoltes[i].cost)
        qtt_rec.append(recoltes[i].qtt_recommandee)

    pris = [0 for i in range(0,len(id[:]))]

    # données de test
    id =       [2,2,2,1,3,3,3,3,8,5,5,6,4,4,4] #id des produits disponibles
    prix =     [2,2,2,3,4,4,4,4,8,7,7,1,3,3,3] #prix du produit
    qtt_rec =  [2,2,2,1,3,3,3,3,8,5,5,6,4,4,4] #quantité recommandée
    pris =     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #indique si le produit est pris

    solde = current_user.balance #argent que dispose le client
    panier = suggestion_panier(pris,False,prix,qtt_rec,solde,id) # false = maximise diversité et true = maximise le poids

    poids = valeur_panier(qtt_rec,panier)
    prix = valeur_panier(prix,panier)
    liste = listingProducts(listeProduits(id,panier))

    return render_template('suggestion.html',
                            jardin = jardin,
                            user = current_user,
                            recoltes = recoltes[:],
                            panier = liste,
                            prix = prix,
                            poids = poids
                            )

def listingProducts(liste):
    tab = []
    for i in range(0,len(liste)):
        produit = Catalogue.query.filter_by(idCatalogue=liste[i]).first()
        tab.append(produit.name)
    return tab
        

def valeur_panier(valeurs,pris): # retourne la valeur du panier (prix)
    somme = 0
    if(pris == []):
        return somme
    for i in range(0,len(valeurs)) :
        if pris[i]==1 :
            somme += valeurs[i]
    return somme

def listeProduits(id,pris): # retourne la liste des produits du panier
    tab = []
    for i in range(0,len(pris)) :
        if pris[i]==1 :
            tab.append(id[i])
    return tab

def plus_diversifie(id,pris):
    return len(list(set(listeProduits(id,pris)))) # élimine les doublons et renvoie la longueur de la lise des produits

def suggestion_panier(list,maximiser_poids,prix,qtt_rec,solde,id) :
    allocation = [[]]
    def suggestion(list,index,maximiser_poids,prix,qtt_rec,solde,id):
        if len(list)!=index:
            for i in range(0,2):
                copy = list[:]
                list[index] = i
                if(valeur_panier(prix,list)<=solde) :
                    if(maximiser_poids):
                        if(valeur_panier(qtt_rec,list)>=valeur_panier(qtt_rec,allocation[0])):
                            allocation[0] = list
                    else :
                        if(plus_diversifie(id,list)>=plus_diversifie(id,allocation[0])):
                            allocation[0] = list
                    suggestion(list,index+1,maximiser_poids,prix,qtt_rec,solde,id)
                list = copy
    suggestion(list,0,maximiser_poids,prix,qtt_rec,solde,id)
    return allocation[0]