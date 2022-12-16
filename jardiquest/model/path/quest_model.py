from flask import request, render_template, redirect, url_for, session
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from datetime import date

def list_garden_quest_model(userId: int):
    user_id = session.get("_user_id")
    if user_id is None:
        return redirect(url_for("controller.login"))
    user = User.query.get(user_id)
    if not user.idJardin :
        # TODO : redirect to a page to create a garden or to join one
        pass
    else:
        id_garden = user.idJardin
        garden = Jardin.query.get(id_garden)
        quests = Quete.query.filter_by(id_jardin=id_garden).all()
        return render_template("quests_list.html", quests=quests, today = date.today(), garden = garden)