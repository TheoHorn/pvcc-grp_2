from jardiquest.setup_sql import db


class Quete(db.Model):
    idQuete = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100), default = "")
    description = db.Column(db.String(1000), default = "")
    periodicity = db.Column(db.Integer(),default = 0)
    sum = db.Column(db.Float(),default = 0.00)
    estimatedTime = db.Column(db.Date())
    startingDate = db.Column(db.Date())
    expiration = db.Column(db.Date())
    
    def get_id(self):
        return self.idQuete
