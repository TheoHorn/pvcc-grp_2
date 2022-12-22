from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_required
from . import app


def get_connected_user_id():
    """Returns the id of the connected user or redirect to login page if not connected"""
    user_id = session.get("_user_id")
    print(user_id)
    if user_id is None:
        return redirect(url_for("controller.login"))
    else:
        return user_id

@app.get("/garden/quests")
@login_required
def list_garden_quests():
    """List all quests of the garden"""
    user_id = get_connected_user_id()
    from jardiquest.model.path.quest_model import list_garden_quest_model
    return list_garden_quest_model(user_id)


@app.get("/my_quests")
@login_required
def list_user_quests():
    """List all quests accepted by the user"""
    user_id = get_connected_user_id()
    from jardiquest.model.path.quest_model import list_user_quests_model
    return list_user_quests_model(user_id)



@app.get("/quest/<string:quest_id>")
@login_required
def display_quest(quest_id):
    """Display a quest with a specific id"""
    from jardiquest.model.path.quest_model import display_quest_model
    return display_quest_model(quest_id)

@app.post("/quest/<string:quest_id>/accept")
@login_required
def accept_quest(quest_id):
    """Accept a quest with a specific id"""
    user_id = get_connected_user_id()
    from jardiquest.model.path.quest_model import accept_quest_model
    return accept_quest_model(user_id, quest_id)

@app.post("/quest/<string:quest_id>/cancel")
@login_required
def cancel_quest(quest_id):
    """Cancel a quest with a specific id"""
    user_id = get_connected_user_id()
    from jardiquest.model.path.quest_model import cancel_quest_model
    return cancel_quest_model(user_id, quest_id)

@app.post("/quest/<string:quest_id>/complete")
@login_required
def complete_quest(quest_id):
    """Complete a quest with a specific id"""
    user_id = get_connected_user_id()
    from jardiquest.model.path.quest_model import complete_quest_model
    return complete_quest_model(user_id, quest_id)