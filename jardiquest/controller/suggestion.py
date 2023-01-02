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

    solde = current_user.balance #argent que dispose le client
    panier = glouton_solution(recoltes,solde)
    prix = prixPanier(panier)

    return render_template('suggestion.html',jardin = jardin,user = current_user,recoltes = recoltes[:],panier = panier,prix = prix)

def prixPanier(panier):
    somme = 0
    for i in range(0,len(panier)):
        somme = somme + panier[i][1]
    return somme
    
def glouton_solution(recoltes,solde) :
    tab = []

    for i in range(0,len(recoltes[:])): # création de lots en fonction de la quantité recommandée
        for j in range(0,int(recoltes[i].quantity/recoltes[i].qtt_recommandee)):
            tab.append([recoltes[i].idCatalogue,(recoltes[i].cost/recoltes[i].quantity)*recoltes[i].qtt_recommandee,recoltes[i].qtt_recommandee,recoltes[i].idRecolte])

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
    memoire = ''
    panier = []
    for i in range(0,len(liste)):
        if(liste[i][0]!=memoire):
            memoire = liste[i][0]
            panier.append(liste[i])
            liste[i]=0
    liste = [value for value in liste if value != 0]

    if(liste!=[]):   
        return triLoop(liste,last+panier)
    else :
        return last+panier