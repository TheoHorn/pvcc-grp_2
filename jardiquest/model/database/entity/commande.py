from jardiquest.setup_sql import db


class Commande(db.Model):
    __tablename__ = "commande"

    idCommande = db.Column(db.String(100), primary_key=True)
    quantite = db.Column(db.Integer, nullable=False)
    dateAchat = db.Column(db.Date, nullable=False)
    traitee = db.Column(db.Boolean, default=False)

    acheteur = db.Column(db.String(100), db.ForeignKey("user.email"), nullable=False)
    recolte = db.Column(db.String(10), db.ForeignKey("recolte.idRecolte"), nullable=False)
    

    def get_id(self):
        return self.idCatalogue
