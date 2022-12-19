from flask import render_template
from flask_login import current_user, login_required
from jardiquest.controller import app
from jardiquest.setup_sql import db
from flask import request
from flask_login import login_required
from . import app
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.annonce import Annonce
from jardiquest.model.database.entity.recolte import Recolte

@app.get('/garden')
@login_required
def garden():
    jardins = Jardin.query.all()
    return render_template('garden.html', user=current_user, jardins=jardins)

@app.get("/new")
@login_required
def new_garden():
    return render_template("new_garden.html", user=current_user)