from jardiquest.setup_sql import db


class Quete(db.Model):
    __tablename__ = "quete"

    idQuete = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100), default="")
    description = db.Column(db.String(1000), default="")
    periodicity = db.Column(db.Integer(), default=0)
    reward = db.Column(db.Float(), default=0.00)
    estimatedTime = db.Column(db.Integer)
    startingDate = db.Column(db.Date())
    timeBeforeExpiration = db.Column(db.Integer)
    id_jardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"))

    user = db.relationship("Accepte", back_populates="quete")
    
    
    def get_id(self):
        return self.idQuete
