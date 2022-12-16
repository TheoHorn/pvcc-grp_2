from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from jardiquest.model.database.entity.user import User
from jardiquest.model.database.entity.jardin import Jardin

def print_garden():
    jar = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if not jar:
        return render_template('handle_garden.html', jardin=jar,user=current_user,notexist=True)
    else:
        return render_template('handle_garden.html', jardin=jar,user=current_user)

