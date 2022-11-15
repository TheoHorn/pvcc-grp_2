from jardiquest.setup_sql import db

class Accepte(db.Model):
    ended = db.Column(db.Boolean())

    def get_id(self):
        return self.idRecolte
