from flask import render_template, Blueprint, request, jsonify
from app.models.usuarios import Usuario
from app.models.models_roles import Administrador, Recolector, Proveedor
from app.models.models_barrios import Comuna
from flask_login import login_required
from app.models import db

admin = Blueprint('admin', __name__)


def crear_usuario(id, nombre, rol, contrasena):
    nuevo_usuario = Usuario(id=id,nombre=nombre,rol=rol)
    nuevo_usuario.ingresar_contrasena(contrasena)

    return nuevo_usuario

@admin.route('/admin_home')
@login_required
def admin_home():
    return render_template('administrador.html')


#LEER
@admin.route('/administradores')
@login_required
def administradores():
    return render_template('administradores.html')

@admin.route('/cargar_administradores', methods=['GET'])
@login_required
def cargar_administradores():
    administradores = Administrador.query.all()
    administradores_list = [{
        'id': admin.id_admin,
        'nombre': admin.nombre,
        'correo': admin.correo,
        'celular': admin.celular,
        'estado': admin.estado
    } for admin in administradores]

    return jsonify(administradores_list)

#CREAR
@admin.route('/nuevo_administrador',methods=['GET','POST'])
@login_required
def nuevo_administrador():
    data = request.get_json()

    id = data.get('id')
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    contrasena = 'admin123'
    rol = 'ADMINISTRADOR'

    user = Usuario.query.filter_by(id=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,rol,contrasena)
    nuevo_admin = Administrador(id_admin=int(id),nombre=nombre,correo=correo,celular=telefono)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_admin)
    db.session.commit()

    return jsonify({'success': True})


#LEER
@admin.route('/recolectores')
@login_required
def recolectores():
    comunas = Comuna.query.all()
    return render_template('recolectores.html',comunas=comunas)

@admin.route('/cargar_recolectores', methods=['GET'])
@login_required
def cargar_recolectores():
    recolectores = Recolector.query.all()
    recolectores_list = [{
        'id': recolector.id_recolector,
        'nombre': recolector.nombre,
        'correo': recolector.correo,
        'celular': recolector.celular,
        'comuna': recolector.comuna,
        'estado': recolector.estado
    } for recolector in recolectores]

    return jsonify(recolectores_list)

#CREAR
@admin.route('/nuevo_recolector',methods=['GET','POST'])
@login_required
def nuevo_recolector():
    data = request.get_json()

    id = data.get('id')
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    comuna = data.get('comuna')
    barrio = data.get('barrio')
    contrasena = 'reco123'
    rol = 'RECOLECTOR'

    user = Usuario.query.filter_by(id=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,rol,contrasena)
    nuevo_recolector = Recolector(id_recolector=int(id),nombre=nombre,direccion=direccion,comuna=comuna,barrio=barrio,correo=correo,celular=telefono)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_recolector)
    db.session.commit()

    return jsonify({'success': True})

@admin.route('/proveedores')
@login_required
def proveedores():
    return render_template('proveedores.html')


    
#CREAR
@admin.route('/nuevo_proveedor',methods=['GET','POST'])
@login_required
def nuevo_proveedor():
    data = request.get_json()

    id = data.get('id')
    tipo = data.get('tipo')
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    comuna = data.get('comuna')
    barrio = data.get('barrio')
    contrasena = 'prov123'
    rol = 'PROVEEDOR'

    user = Proveedor.query.filter_by(id=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,rol,contrasena)
    nuevo_proveedor = Proveedor(id_proveedor=int(id),tipo_prov=tipo,nombre=nombre,direccion=direccion,id_comuna=comuna,id_barrio=barrio,correo=correo,celular=telefono)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_proveedor)
    db.session.commit()

    return jsonify({'success': True})