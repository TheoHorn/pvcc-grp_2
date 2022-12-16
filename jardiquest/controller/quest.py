from flask import request, render_template, redirect, url_for, session
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from datetime import date
from . import app


# ------------------------------------------ Garden quests ------------------------------------------
@app.get("/garden/<int:id_garden>/quests")
def list_garden_id_quests(id_garden):
    """List all quests of a specific garden"""
    print(session)
    garden = Jardin.query.get(id_garden)
    quests = Quete.query.filter_by(id_jardin=id_garden).all()
    return render_template("quests_list.html", quests=quests, today = date.today(), garden = garden)


@app.get("/garden/quests")
def list_garden_quests():
    """List all quests of the garden"""
    user_id = session.get("_user_id")
    if user_id is None:
        return redirect(url_for("controller.login"))
    else:
        from jardiquest.model.path.quest_model import list_garden_quest_model
        return list_garden_quest_model(user_id)



# ------------------------------------------ User quests ------------------------------------------
@app.get("/my_quests")
def list_my_quests():
    """List all quests accepted by the user"""
    id = 1 # TODO get the id of the connected user
    quests = Quete.query.filter_by(user=id).all()
    pass



# ------------------------------------------ Quests Details ------------------------------------------
@app.get("/quest/<int:quest_id>")
def display_quest(quest_id):
    """Display a quest with a specific id"""
    quest = Quete.query.get(quest_id)
    return quest