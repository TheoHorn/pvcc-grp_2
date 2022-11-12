from jardiquest.setup_sql import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def get_id(self):
        return self.id

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_authenticated():
        return True
