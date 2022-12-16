from flask import render_template, redirect, url_for, session
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from datetime import date




def getUser(user_id: int):
    """Get the user with the id user_id or redirect to login page if not connected"""
    if user_id is None:
        return redirect(url_for("controller.login"))
    else:
        return User.query.get(user_id)

# ------------------------------------------ Garden quests ------------------------------------------

def list_garden_id_quest_model(gardenId : int):
    garden = Jardin.query.get(gardenId)
    quests = Quete.query.filter_by(id_jardin=gardenId).all()
    return render_template("quests_list.html", quests=quests, today = date.today(), garden = garden)


def list_garden_quest_model(user_id: str):
    user = getUser(user_id)
    if not user.idJardin :
        # TODO : redirect to a page to create a garden or to join one
        pass
    else:
        id_garden = user.idJardin
        garden = Jardin.query.get(id_garden)
        quests = Quete.query.filter_by(id_jardin=id_garden).all()
        return render_template("quests_list.html", quests=quests, today = date.today(), garden = garden)


# ------------------------------------------ User quests ------------------------------------------
def list_user_quests_model(user_id: str):
    user = getUser(user_id)
    quests = Quete.query.filter_by(id_user=user_id).all()
    # TODO view to display the quests of the user
    pass





# ------------------------------------------ Quests Details ------------------------------------------
def display_quest_model(quest_id: int):
    """Display a quest with a specific id"""
    quest = Quete.query.get(quest_id)
    return render_template("quest_detaills.html", quest=quest, today = date.today())