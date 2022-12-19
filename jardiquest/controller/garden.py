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
# TODO create filter
@app.get('/garden')
@login_required
def garden():
    jardins = Jardin.query.all()
    jar = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    return render_template('garden.html', user=current_user, jardins=jardins, jardin=jar)

# create a new garden (owner)
@app.route('/new',methods=['GET', 'POST'])
@login_required
def new_garden():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        monnaie = request.form['monnaie']
        capacite = request.form['capacite']
        
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

        # create it
        new_garden = Jardin(idJardin=generateId(nom), name=nom, moneyName=monnaie)
        db.session.add(new_garden)
        db.session.commit()

        # update user status
        current_user.update_garden(nom)
        db.session.commit()

        return redirect(url_for('controller.garden'))
        
    return render_template("new_garden.html", user=current_user)

@app.route('/<choose>')
def choose(choose):
    jar = Jardin.query.filter_by(idJardin=choose).first()
    flash(f"Vous avez rejoint le jardin \"{jar.name}\"")

    # update user status
    current_user.update_garden(choose)
    db.session.commit()
    return redirect(url_for('controller.garden'))   

def generateId(moneyName):
    # TODO improve this function
    num = random.randint(0,99999)
    return moneyName[0:4]+str(num)