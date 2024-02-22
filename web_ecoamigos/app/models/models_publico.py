from . import db
from sqlalchemy import Text, LargeBinary, ForeignKey

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id_noticia      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_admin        = db.Column(db.Integer, nullable=False)
    titulo          = db.Column(db.String(250), nullable=False)
    descripcion     = db.Column(Text, nullable=False)
    fecha           = db.Column(db.DateTime(timezone=True))
    recurso         = db.Column(LargeBinary)

    def editar_publicacion(self, titulo=None, descripcion=None, imagen=None):
        if titulo:
            self.titulo = titulo
        if descripcion:
            self.descripcion = descripcion
        if imagen:
            self.recurso = imagen

class Resena(db.Model):
    __tablename__ = 'resenas'
    id_resena       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor    = db.Column(db.Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    estrellas       = db.Column(db.Integer, nullable=False)
    comentario      = db.Column(Text, nullable=False)

    



