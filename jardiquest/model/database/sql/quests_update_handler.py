from datetime import date, timedelta
from jardiquest.model.database.entity.quete import Quete
from jardiquest.setup_sql import db
from . import scheduler

@scheduler.task('updt_quests', id='updt_quests', seconds=5)  
def update_state_quests():
    quests = Quete.query.filter_by(accomplished=False).all()
    for quest in quests:
        
        if (date.today() - quest.startingDate).days > quest.timeBeforeExpiration:
            # If the quest is expired
            
            if quest.periodicity > 0:
                # If the quest is periodic, we create a new one
                new_quest = Quete(title = quest.title, description = quest.description, periodicity = quest.periodicity, 
                                timeBeforeExpiration = quest.timeBeforeExpiration, reward = quest.reward, id_jardin = quest.id_jardin, 
                                accomplished = False, startingDate = quest.startingDate + timedelta(days=quest.periodicity))
                db.session.add(new_quest)
            else:
                # If the quest is not periodic, we delete it
                db.session.delete(quest)
    print("update")
    db.session.commit()    