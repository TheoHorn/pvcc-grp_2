from http.client import HTTPException

from flask import request,render_template, flash, redirect, url_for
from flask_login import current_user

from jardiquest.controller import handling_status_error
from jardiquest.model.database.entity.user import User
from jardiquest.model.database.entity.jardin import Jardin

def print_garden():
    jar = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    par = User.query.filter_by(idJardin=current_user.idJardin)
    if not jar:
        return render_template('handle_garden.html', jardin=jar,user=current_user,notexist=True)
    else:
        return render_template('handle_garden.html', jardin=jar,participant=par,user=current_user)



def handle_garden_handler_model(methods: str):

    if methods == 'put':
        name = request.form.get('name')
        moneyName = request.form.get('new_password')
        return update_model_garden(name, moneyName)
    elif methods == 'delete':
        return delete_model_garden()
    else:
        return handling_status_error(HTTPException(404))


def update_model_garden(name:str,nameMoney:str):
    if name != None and nameMoney != None:
        Jardin.update().values({"name": name,"moneyName": nameMoney})

# a coder
def delete_model_garden():
    return False