from flask import render_template, redirect, url_for, session, abort
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db
from datetime import date, timedelta




def getUser(user_id: int):
    """Get the user with the id user_id or redirect to login page if not connected"""
    if user_id is None:
        return redirect(url_for("controller.login"))
    else:
        return User.query.get(user_id)

# ------------------------------------------ Garden quests ------------------------------------------

def list_garden_quest_model(user_id: str):
    user = getUser(user_id)
    if not user.idJardin :
        return redirect(url_for("controller.garden"))
    else:
        id_garden = user.idJardin
        garden = Jardin.query.get(id_garden)
        quests = Quete.query.filter_by(id_jardin=id_garden, id_user = None).all()
        quests.sort(key=lambda x: x.timeBeforeExpiration - (date.today() - x.startingDate).days)
        quests = [quest for quest in quests if not ((date.today() - quest.startingDate).days > quest.timeBeforeExpiration)]
        return render_template("quests_list_garden.html", quests=quests, today = date.today(), garden = garden)


# ------------------------------------------ User quests ------------------------------------------
def list_user_quests_model(user_id: str):
    user = getUser(user_id)
    if not user.idJardin :
        return redirect(url_for("controller.garden"))
    garden = Jardin.query.get(user.idJardin)
    quests = user.quetes
    quests = [quest for quest in quests if not quest.accomplished]
    quests.sort(key=lambda x: x.timeBeforeExpiration - (date.today() - x.startingDate).days)
    return render_template("quests_list_user.html", quests=quests, today = date.today(), user = user, garden=garden)


def accept_quest_model(user_id: str, quest_id: int):
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    print(quest.accomplished)
    if quest.id_jardin == user.idJardin:
        quest.id_user = user_id
        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_garden_quests"))


def cancel_quest_model(user_id: str, quest_id: int):
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == user.idJardin:
        quest.id_user = None
        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_user_quests"))



def complete_quest_model(user_id: str, quest_id: int):
    # TODO change if we want the garden manager to validate the quest
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == user.idJardin:
        quest.accomplished = True
        user.balance += quest.reward

        # If the quest is periodic, we create a new one
        if quest.periodicity :
            new_quest = Quete(title = quest.title, description = quest.description, peridiodicity = quest.periodicity, 
                            timeBeforeExpiration = quest.timeBeforeExpiration, reward = quest.reward, id_jardin = quest.id_jardin, 
                            accomplished = False,  startingDate = quest.startingDate + timedelta(days=quest.periodicity))
            db.session.add(new_quest)

        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_user_quests"))



# ------------------------------------------ Quests Details ------------------------------------------
def display_quest_model(quest_id: int):
    """Display a quest with a specific id"""
    user_id = session.get("_user_id")
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if not quest.id_jardin == user.idJardin:
        abort(403)
    garden = Jardin.query.get(quest.id_jardin)
    return render_template("quest_details.html", quest=quest, today = date.today(), garden = garden, user = user_id)

