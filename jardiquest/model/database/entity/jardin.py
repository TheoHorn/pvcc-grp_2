from jardiquest.setup_sql import db

class Jardin(db.Model):
    idJardin = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    moneyName = db.Column(db.String(100), default="Monnaie")

    def get_id(self):
        return self.idCatalogue
