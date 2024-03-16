from . import db
from app import bcrypt
from flask_login import UserMixin
from app import login_manager

@login_manager.user_loader
def cargar_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id          = db.Column(db.String(250), primary_key=True)
    nombre      = db.Column(db.String(20), nullable=False)
    correo      = db.Column(db.String(250), nullable=False)
    contrasena  = db.Column(db.String(250), nullable=False)
    rol         = db.Column(db.String(20), nullable=False)
    estado      = db.Column(db.Boolean, default=True)

    def ingresar_contrasena(self, contrasena):
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    def verificar_contrasena(self, contrasena):
        return bcrypt.check_password_hash(self.contrasena, contrasena)
    
    def cambiar_contrasena(self, contrasena_actual, contrasena_nueva):
        if self.verificar_contrasena(contrasena_actual):
            self.ingresar_contrasena(contrasena_nueva)

            return True
        else:
            return False
        
    def actualizar_usuario(self, nombre=None, correo=None):
        if nombre:
            self.nombre = nombre
        if correo:
            self.correo = correo


    
    def desactivar_usuario(self):
        self.estado = False
    

    
    
