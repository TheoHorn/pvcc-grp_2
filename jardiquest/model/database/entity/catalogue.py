from jardiquest.setup_sql import db


class Catalogue(db.Model):
    __tablename__ = "catalogue"

    idCatalogue = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), default="")   
    
    recolte = db.relationship("Recolte", back_populates="catalogue")

    def get_id(self):
        return self.idCatalogue
