from jardiquest.setup_sql import db


class User(db.Model):
    idUser = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(15), default = "Participant")
    balance = db.Column(db.Float(), default = 0.00)
    idJardin = db.Column(db.Date())

    def get_id(self):
        return self.idUser

    @staticmethod
    def is_active():
        return False

    @staticmethod
    def is_authenticated():
        return True
