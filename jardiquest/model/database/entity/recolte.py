from jardiquest.setup_sql import db

class Recolte(db.Model):
    idRecolte = db.Column(db.String(10), primary_key=True)
    quantity = db.Column(db.Integer(), default = 0)
    date = db.Column(db.Date())
    cost = db.Column(db.Float(),default = 0.00)
    

    def get_id(self):
        return self.idRecolte
