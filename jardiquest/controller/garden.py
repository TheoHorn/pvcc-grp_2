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
import random

# show all gardens
@app.route('/garden',methods=['GET', 'POST'])
@login_required
def garden():
    jardin_de_user = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    # all the gardens he can access
    if jardin_de_user is not None :
        jardins = Jardin.query.filter(Jardin.idJardin != jardin_de_user.idJardin)
    else :
        jardins = Jardin.query.all()
    if request.method == 'POST':
        nom = request.form['filtreNom']
        description = request.form['filtreDescription']
        monnaie = request.form['filtreMonnaie']
        ville = request.form['filtreVille']
        adresse = request.form['filtreAdresse']

        name = "%{}%".format(nom)
        monnaie = "%{}%".format(monnaie)
        description = "%{}%".format(description)
        ville = "%{}%".format(ville)
        adresse = "%{}%".format(adresse)

        if jardin_de_user is not None :
            jardins = Jardin.query.filter(Jardin.name.like(name),
                Jardin.idJardin != jardin_de_user.idJardin,
                Jardin.moneyName.like(monnaie),
                Jardin.description.like(description),
                Jardin.ville.like(ville),
                Jardin.adresse.like(adresse)
                ).all()
        else :
            jardins = Jardin.query.filter(Jardin.name.like(name), Jardin.moneyName.like(monnaie)).all()

    total = len(jardins[:])
    displayed = len(jardins[0:19])
    return render_template('garden.html', user=current_user, jardins=jardins[0:19], jardin=jardin_de_user, displayed=displayed, total=total)

# create a new garden (owner)
@app.route('/new',methods=['GET', 'POST'])
@login_required
def new_garden():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        monnaie = request.form['monnaie']
        adresse = request.form['adresse']
        ville = request.form['ville']
        
        # verification if name and money are unique
        jar = Jardin.query.filter_by(name=nom).first()
        mon = Jardin.query.filter_by(moneyName=monnaie).first()
        error = False

        if jar is not None :
            flash(f"Le nom de jardin \"{nom}\" existe déjà")
            error = True
        if mon is not None :
            flash(f"Le nom de monnaie \"{monnaie}\" existe déjà")
            error = True

        if error :
            return redirect(url_for('controller.new_garden'))

        id = generateId(nom)

        # create it
        new_garden = Jardin(idJardin=id, name=nom, moneyName=monnaie, description=description, adresse=adresse, ville=ville)
        db.session.add(new_garden)
        
        # update user status
        current_user.update_garden(id)
        current_user.update_role('Proprietaire')
        current_user.update_balance(0)
        db.session.commit()

        return redirect(url_for('controller.garden'))
        
    return render_template("new_garden.html", user=current_user)

@app.route('/change/<choose>')
def choose(choose):
    jar = Jardin.query.filter_by(idJardin=choose).first()
    flash(f"Vous avez rejoint le jardin \"{jar.name}\" en tant que participant")
 
    # update user status
    current_user.update_garden(choose)
    current_user.update_balance(0)
    db.session.commit()
    return redirect(url_for('controller.garden'))   

@app.route('/leave')
def leave():
    current_user.update_garden('')
    db.session.commit()
    flash(f"Vous avez quitté le jardin")
    return redirect(url_for('controller.garden'))  

@app.route('/delete')
def delete():
    Jardin.query.filter(Jardin.idJardin == current_user.idJardin).delete()
    current_user.update_garden('')
    current_user.update_role('Participant')
    db.session.commit()
    flash(f"Vous avez supprimé votre jardin")
    return redirect(url_for('controller.garden')) 

def generateId(moneyName):
    # TODO improve this function
    num = random.randint(0,99999)
    return moneyName[0:4]+str(num)

# create a new garden (owner)
@app.route('/modify',methods=['GET', 'POST'])
@login_required
def modify_garden():
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        monnaie = request.form['monnaie']
        adresse = request.form['adresse']
        ville = request.form['ville']
        
        garden = Jardin.query.filter_by(idJardin=jardin.idJardin).first()
        own_name = garden.name
        own_money = garden.moneyName
        
        error = False

        # if the name if modified --> verify if already exists
        if nom != own_name :
            jar = Jardin.query.filter(Jardin.idJardin != jardin.idJardin, Jardin.name==nom).first()
            if jar is not None :
                flash(f"Le nom de jardin \"{nom}\" existe déjà")
                error = True

        # if the money if modified --> verify if already exists
        if monnaie != own_money :
            mon = Jardin.query.filter(Jardin.idJardin != jardin.idJardin, Jardin.moneyName==monnaie).first()
            if mon is not None :
                flash(f"Le nom de monnaie \"{monnaie}\" existe déjà")
                error = True
        
        if error :
            return redirect(url_for('controller.modify_garden'))

        # modify it
        jardin.update_name(nom)
        jardin.update_description(description)
        jardin.update_money(monnaie)
        jardin.update_address(adresse)
        jardin.update_city(ville)
        
        db.session.commit()

        flash(f"Le jardin a été modifié avec succès")
        return redirect(url_for('controller.garden'))
        
    return render_template("modify_garden.html", user=current_user, jardin=jardin)