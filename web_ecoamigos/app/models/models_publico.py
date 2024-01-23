from . import db, func
from sqlalchemy import Text, LargeBinary, ForeignKey

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id_noticia      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_admin        = db.Column(db.Integer, ForeignKey('administradores.id_admin'), nullable=False)
    titulo          = db.Column(db.String(250), nullable=False)
    descripcion     = db.Column(Text, nullable=False)
    fecha           = db.Column(db.DateTime(timezone=True), default=func.now())
    recurso         = db.Column(LargeBinary, nullable=False)

    @classmethod
    def agregar_noticia(cls, noticia_data):
        nueva_noticia = cls(**noticia_data)
        db.session.add(nueva_noticia)
        db.session.commit()

class Resena(db.Model):
    __tablename__ = 'resenas'
    id_resena       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor    = db.Column(db.Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    estrellas       = db.Column(db.Integer, nullable=False)
    comentario      = db.Column(Text, nullable=False)

    



