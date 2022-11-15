from jardiquest.setup_sql import db

class Annonce(db.Model):
    idAnnonce = db.Column(db.String(10), primary_key=True)
    timestamps = db.Column(db.Date())
    message = db.Column(db.String(1000),default="")
    

    def get_id(self):
        return self.idAnnonce
