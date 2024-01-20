from . import db

class Comuna(db.Model):
    __tablename__ = 'comunas'
    id_comuna   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comuna      = db.Column(db.String(20), nullable=False)

class Barrio(db.Model):
    __tablename__ = 'barrios'
    id_barrio   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comuna   = db.Column(db.Integer, nullable=False)
    nombre      = db.Column(db.String(), nullable=False)


