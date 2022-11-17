from jardiquest.setup_sql import db


class Jardin(db.Model):
    __tablename__ = "jardin"

    idJardin = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    moneyName = db.Column(db.String(100), default="Monnaie")

    recolte = db.relationship("Recolte", back_populates="jardin")
    annonce = db.relationship("Annonce", back_populates="jardin", uselist=False)
    user = db.relationship("User", back_populates="jardin")

    def get_id(self):
        return self.idCatalogue
