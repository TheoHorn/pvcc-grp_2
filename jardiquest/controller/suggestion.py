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

@app.route('/sug')
@login_required
def suggestion():    
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if jardin is not None :
        recoltes = Recolte.query.filter(Recolte.idJardin == jardin.idJardin)
    else :
        recoltes = []
    return render_template('suggestion.html',jardin = jardin, user = current_user, recoltes = recoltes[:])