from . import db
class Administrador(db.Model):
    __tablename__ = 'administradores'
    id_admin    = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre      = db.Column(db.String(250), nullable=False)
    correo      = db.Column(db.String(250),nullable=False)
    celular     = db.Column(db.BigInteger, nullable=False)
    estado      = db.Column(db.Boolean, default=True)

    def actualizar_datos(self, nuevos_datos):
        self.nombre     = nuevos_datos.get('nombre', self.nombre)
        self.correo     = nuevos_datos.get('correo', self.correo)
        self.celular    = nuevos_datos.get('nombre', self.nombre)

    def desactivar_usuario(self):
        self.estado = False

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
    puntos          = db.Column(db.Integer)
    estado          = db.Column(db.Boolean, default=True)

    def actualizar_datos(self, nuevos_datos):
        self.nombre         = nuevos_datos.get('nombre', self.nombre)
        self.direccion      = nuevos_datos.get('direccion', self.direccion)
        self.id_comuna      = nuevos_datos.get('comuna', self.id_comuna)
        self.id_barrio      = nuevos_datos.get('barrio', self.id_barrio)
        self.correo         = nuevos_datos.get('correo', self.correo)
        self.celular        = nuevos_datos.get('celular', self.celular)

    def desactivar_usuario(self):
        self.estado = False

    def aumentar_puntos(self,nuevos_puntos):
        puntos = self.puntos + nuevos_puntos
        self.puntos = puntos
    def restar_puntos(self,nuevos_puntos):
        puntos = self.puntos - nuevos_puntos
        self.puntos = puntos

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

    def actualizar_datos(self, nuevos_datos):
        self.nombre         = nuevos_datos.get('nombre', self.nombre)
        self.direccion      = nuevos_datos.get('direccion', self.direccion)
        self.comuna         = nuevos_datos.get('comuna', self.comuna)
        self.barrio         = nuevos_datos.get('barrio', self.barrio)
        self.correo         = nuevos_datos.get('correo', self.correo)
        self.celular        = nuevos_datos.get('celular', self.celular)

    def desactivar_usuario(self):
        self.estado = False








