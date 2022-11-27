from flask import request, render_template, redirect, url_for
from jardiquest.model.database.entity.quete import Quete
from . import app

@app.get("/quests")
def list__all_quests():
    """TODO delete, test"""
    quests = Quete.query.all()
    return quests

@app.get("/quests/<int:quest_id>")
def display_quest(quest_id):
    """Display a quest with a specific id"""
    quest = Quete.query.get(quest_id)
    return quest


@app.get("/quests/create_quest")
def create_quest_get():
    """
    Display a form to create a quest
    """
    return render_template("create_quest.html")


@app.post("/quests/create_quest")
def create_quest_post():
    """Create a quest
    TODO delete when finish testing"""
    title = request.form.get("title")
    description = request.form.get("description")
    sum = request.form.get("sum")
    periodicity = request.form.get("periodicity")
    estimatedTime = request.form.get("estimatedTime")
    startingDate = request.form.get("startingDate")
    expiration = request.form.get("expiration")
    quest = Quete(title=title, description=description, sum=sum, periodicity=periodicity, estimatedTime=estimatedTime, startingDate=startingDate, expiration=expiration)
    quest.save()
    return redirect(url_for("display_quest", quest_id=quest.id))