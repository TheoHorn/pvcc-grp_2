from jardiquest.setup_sql import db

class Accepte(db.Model):
    __tableName__= "accepte"
    
    email = db.Column(db.String(100),db.ForeignKey("user.email"), primary_key=True)
    idQuete = db.Column(db.String(10),db.ForeignKey("quete.idQuete"), primary_key=True)
    ended = db.Column(db.Boolean(), default=False)

    user = db.relationship("User", back_populates="quete")
    quete = db.relationship("Quete", back_populates="user")
