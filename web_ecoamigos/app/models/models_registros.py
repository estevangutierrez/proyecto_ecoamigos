from . import db, func
from sqlalchemy import ForeignKey

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    id_solicitud    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor    = db.Column(db.Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=func.now())
    cantidad_aprox  = db.Column(db.Integer, nullable=False)
    estado          = db.Column(db.String(20), nullable=False, default='pendiente')
    detalle         = db.Column(db.String(250))

    def aceptar_solicitud(self, id_recolector):
        self.estado = id_recolector

class Visita(db.Model):
    __tablename__ = 'visitas'
    id_visita           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_solicitud        = db.Column(db.Integer, ForeignKey('solicitudes.id_solicitud'), nullable=False)
    id_recolector       = db.Column(db.Integer, ForeignKey('recolectores.id_recolector'), nullable=False)
    fecha_recoleccion   = db.Column(db.DateTime(timezone=True), default=func.now())
    cant_recolectada    = db.Column(db.Integer, nullable=False)
    costo               = db.Column(db.Integer, nullable=False)
    
class Certificado(db.Model):
    __tablename__ = 'certificados'
    id_certificado  = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_proveedor    = db.Column(db.Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    id_admin        = db.Column(db.Integer, ForeignKey('administradores.id_admin'), nullable=False)
    fecha           = db.Column(db.DateTime, default=func.now())
    tipo            = db.Column(db.String(15), nullable=False)
    
          


