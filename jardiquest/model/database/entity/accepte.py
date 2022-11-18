from jardiquest.setup_sql import db

class Accepte(db.Model):
    __tableName__= "accepte"
    
    idUser = db.Column(db.ForeignKey("user.idUser"), primary_key=True)
    idQuete = db.Column(db.ForeignKey("quete.idQuete"), primary_key=True)
    ended = db.Column(db.Boolean(), default=False)

    user = db.relationship("User", backref="quete")
    quete = db.relationship("Quete", backref="user")
