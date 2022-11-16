from jardiquest.setup_sql import db

accepte_table = db.Table(
    "accepte",
    db.Base.metadata,
    db.Column("idUser", db.ForeignKey("user.idUser"), primary_key=True),
    db.Column("idQuete", db.ForeignKey("quete.idQuete"), primary_key=True),
    db.Column("ended",db.Boolean(),default=False)
    )

class User(db.Model):
    __tablename__ = "user"

    idUser = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(15), default="Participant")
    balance = db.Column(db.Float(), default=0.00)
    recruitmentDate = db.Column(db.Date())

    idJardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"))
    jardin = db.relationship("Jardin", back_populates="user")

    annonce = db.relationship("Annonce", back_populates="user")

    quete = db.relationship("Quete", secondary=accepte_table, backref="user")

    def get_id(self):
        return self.idUser

    @staticmethod
    def is_active():
        return False

    @staticmethod
    def is_authenticated():
        return True
