from flask import render_template, redirect, url_for, session, abort
from flask_login import current_user
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db
from datetime import date, timedelta
import uuid




# ------------------------------------------ Garden quests ------------------------------------------

def list_garden_quest_model():
    if not current_user.idJardin :
        return redirect(url_for("controller.garden"))
    else:
        id_garden = current_user.idJardin
        garden = Jardin.query.get(id_garden)
        quests = Quete.query.filter_by(id_jardin=id_garden, id_user = None).all()
        quests.sort(key=lambda x: x.timeBeforeExpiration - (date.today() - x.startingDate).days)
        quests = [quest for quest in quests if not ((date.today() - quest.startingDate).days > quest.timeBeforeExpiration) and quest.startingDate <=  date.today()]
        return render_template("quests_list_garden.html", quests=quests, today = date.today(), garden = garden)


# ------------------------------------------ User quests ------------------------------------------
def list_user_quests_model():
    if not current_user.idJardin :
        return redirect(url_for("controller.garden"))
    garden = Jardin.query.get(current_user.idJardin)
    quests = current_user.quetes
    quests = [quest for quest in quests if not quest.accomplished]
    quests.sort(key=lambda x: x.timeBeforeExpiration - (date.today() - x.startingDate).days and x.startingDate <=  date.today()) 
    return render_template("quests_list_user.html", quests=quests, today = date.today(), user = current_user, garden=garden)


def accept_quest_model(quest_id: int):
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == current_user.idJardin:
        quest.user = current_user
        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_garden_quests"))


def cancel_quest_model(quest_id: int):
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == current_user.idJardin and quest.user == current_user and not quest.accomplished:
        quest.user = None
        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_user_quests"))



def complete_quest_model(quest_id: int):
    # TODO change if we want the garden manager to validate the quest
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == current_user.idJardin and quest.user == current_user and not quest.accomplished:
        quest.accomplished = True
        current_user.balance += quest.reward
        current_user.balance = round(current_user.balance, 2)

        # If the quest is periodic, we create a new one
        if quest.periodicity :
            new_quest = Quete(idQuete= uuid.uuid1().hex, title = quest.title, description = quest.description, periodicity = True, 
                                    timeBeforeExpiration = quest.timeBeforeExpiration, reward = quest.reward, id_jardin = quest.id_jardin, 
                                    accomplished = False, startingDate = quest.startingDate + timedelta(days=quest.timeBeforeExpiration))
            db.session.add(new_quest)

        db.session.commit()
    else :
        abort(403)
    return redirect(url_for("controller.list_user_quests"))



# ------------------------------------------ Quests Details ------------------------------------------
def display_quest_model(quest_id: int):
    """Display a quest with a specific id"""
    quest = Quete.query.get(quest_id)
    if quest.id_jardin != current_user.idJardin or (quest.user != current_user and quest.user != None) or quest.accomplished:
        abort(403)
    garden = Jardin.query.get(quest.id_jardin)
    return render_template("quest_details.html", quest=quest, today = date.today(), garden = garden, user = current_user.email)

