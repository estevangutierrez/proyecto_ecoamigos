from . import db
class Administrador(db.Model):
    __tablename__ = 'administradores'
    id_admin    = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre      = db.Column(db.String(250), nullable=False)
    correo      = db.Column(db.String(250),nullable=False)
    celular     = db.Column(db.BigInteger, nullable=False)
    estado      = db.Column(db.Boolean, default=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id_proveedor    = db.Column(db.Integer, primary_key=True)
    tipo_prov       = db.Column(db.Integer, nullable=False)
    nombre          = db.Column(db.String(250), nullable=False)
    direccion       = db.Column(db.String(250), nullable=False)
    id_comuna       = db.Column(db.Integer, nullable=False)
    id_barrio       = db.Column(db.Integer, nullable=False)
    correo          = db.Column(db.String(250), nullable=False)
    celular         = db.Column(db.BigInteger, nullable=False)
    puntos          = db.Column(db.Integer, nullable=False)
    estado          = db.Column(db.Boolean, default=True)

class Recolector(db.Model):
    __tablename__ = 'recolectores'
    id_recolector   = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(250), nullable=False)
    direccion       = db.Column(db.String(250), nullable=False)
    comuna          = db.Column(db.Integer, nullable=False)
    barrio          = db.Column(db.Integer, nullable=False)
    correo          = db.Column(db.String(250), nullable=False)
    celular         = db.Column(db.BigInteger, nullable=False)
    estado          = db.Column(db.Boolean, default=True)








