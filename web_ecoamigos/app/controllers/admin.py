from flask import render_template, Blueprint, request, jsonify
from app.models.usuarios import Usuario
from app.models.models_roles import Administrador, Recolector, Proveedor
from app.models.models_barrios import Comuna, Barrio
from app.models.models_publico import Noticia
from app.models.models_registros import Solicitud, Visita
from flask_login import login_required
from app import roles_required
from app.models import db

admin = Blueprint('admin', __name__)


def crear_usuario(id, nombre, rol, contrasena):
    nuevo_usuario = Usuario(id=id,nombre=nombre,rol=rol)
    nuevo_usuario.ingresar_contrasena(contrasena)

    return nuevo_usuario

@admin.route('/publicaciones')
@login_required
@roles_required('ADMINISTRADOR')
def publicaciones():
    noticias = reversed(Noticia.query.all())
    return render_template('publicaciones.html', noticias=noticias)

@admin.route('/admin_home')
@login_required
@roles_required('ADMINISTRADOR')
def admin_home():
    return render_template('administrador.html')

@admin.route('/administrador/solicitudes')
@login_required
@roles_required('ADMINISTRADOR')
def solicitudes():
    datos = (
        db.session.query(Solicitud, Proveedor)
        .join(Proveedor, Solicitud.id_proveedor == Proveedor.id_proveedor)
        )
    
    solicitudes_asignadas = (
        db.session.query(Solicitud, Recolector)
        .join(Recolector, Solicitud.estado == Recolector.id_recolector)
        )

    historial_visitas = (
        db.session.query(Visita, Recolector, Proveedor)
        .join(Recolector, Visita.id_recolector == Recolector.id_recolector)
        .join(Proveedor, Visita.id_proveedor == Proveedor.id_proveedor)
        .all()
        )
    
    recolectores_data = Recolector.query.filter_by(estado=True)

    solicitudes = []
    recolectores = []
    solicitudes_a = []
    visitas = []


    for solicitud, proveedor in datos:
        solicitudes_dict = {
            'id': solicitud.id_solicitud,
            'id_proveedor':solicitud.id_proveedor,
            'proveedor':proveedor.nombre,
            'fecha':solicitud.fecha_solicitud,
            'cantidad':solicitud.cantidad_aprox,
            'estado':solicitud.estado
        }

        solicitudes.append(solicitudes_dict)

    for recolector in recolectores_data:
        recolectores_dict = {
            'id':recolector,
            'nombre':recolector.nombre
        }

        recolectores.append(recolectores_dict)

    for solicitud_a, recolector in solicitudes_asignadas:
        asignadas_dict = {
            'id': solicitud_a.id_solicitud,
            'id_proveedor':solicitud_a.id_proveedor,
            'fecha':solicitud_a.fecha_solicitud,
            'cantidad':solicitud_a.cantidad_aprox,
            'asignado': recolector.nombre
        }

        solicitudes_a.append(asignadas_dict)

    for visita, recolector, proveedor in historial_visitas:
        visitas_dict = {
            'id': visita.id_visita,
            'solicitud': visita.id_solicitud,
            'proveedor': proveedor.nombre,
            'recolector': recolector.nombre,
            'fecha': visita.fecha_recoleccion,
            'cantidad': visita.cant_recolectada,
            'valor': visita.costo,
            'puntos': visita.puntos
        }

        visitas.append(visitas_dict)


    return render_template("solicitudes.html", solicitudes=solicitudes, recolectores=recolectores,solicitudes_a=solicitudes_a, visitas=visitas)


#LEER
@admin.route('/administradores')
@login_required
@roles_required('ADMINISTRADOR')
def administradores():
    administradores = Administrador.query.all()
    return render_template('administradores.html', administradores=administradores)

@admin.route('/cargar_administradores', methods=['GET'])
@login_required
@roles_required('ADMINISTRADOR')
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
@roles_required('ADMINISTRADOR')
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

#ACTUALIZAR
@admin.route('/administrador/<int:id_admin>')
@login_required
@roles_required('ADMINISTRADOR')
def actualizar_administrador(id_admin):
    administrador = Administrador.query.get(id_admin)

    if administrador is None:
        return jsonify({'error':'Administrador no encontrado'}), 404
    
    nuevos_datos = request.json
    administrador.actualizar_datos(nuevos_datos)

    try:
        db.session.commit()
        return jsonify({'mensaje': 'Administrador actualizado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el administrador'}), 500
    finally:
        db.session.close()

#LEER
@admin.route('/recolectores')
@login_required
@roles_required('ADMINISTRADOR')
def recolectores():
    comunas = Comuna.query.all()
    barrios = Barrio.query.all()
    recolectores = Recolector.query.all()
    return render_template('recolectores.html',comunas=comunas, recolectores=recolectores, barrios=barrios)

#CREAR
@admin.route('/nuevo_recolector',methods=['GET','POST'])
@login_required
@roles_required('ADMINISTRADOR')
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

@admin.route('/recolector/<int:id_recolector>', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def actualizar_recolector(id_recolector):
    recolector = Recolector.query.get(id_recolector)

    if recolector is None:
        return jsonify({'error':'recolector no encontrado'}), 404
    
    nuevos_datos = request.json
    recolector.actualizar_datos(nuevos_datos)

    try:
        db.session.commit()
        return jsonify({'mensaje': 'recolector actualizado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el recolector'}), 500
    finally:
        db.session.close()

@admin.route('/proveedores')
@login_required
@roles_required('ADMINISTRADOR')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html',proveedores=proveedores)


#CREAR
@admin.route('/nuevo_proveedor',methods=['GET','POST'])
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
    puntos = 0
    rol = 'PROVEEDOR'

    user = Proveedor.query.filter_by(id_proveedor=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,rol,contrasena)
    nuevo_proveedor = Proveedor(id_proveedor=int(id),tipo_prov=int(tipo),nombre=nombre,direccion=direccion,id_comuna=comuna,id_barrio=barrio,correo=correo,celular=telefono,puntos=puntos)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_proveedor)
    db.session.commit()

    return jsonify({'success': True})

@admin.route('/proveedor/<int:id_proveedor>', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def actualizar_proveedor(id_proveedor):
    proveedor = Recolector.query.get(id_proveedor)

    if proveedor is None:
        return jsonify({'error':'Proveedor no encontrado'}), 404
    
    nuevos_datos = request.json
    proveedor.actualizar_datos(nuevos_datos)

    try:
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el proveedor'}), 500
    finally:
        db.session.close()

@admin.route('/administrador/solicitudes/asignar', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def asignar_solicitudes():
    asignaciones = request.get_json()

    recolector = asignaciones.get('recolector').get('id_recolector')
    solicitudes = asignaciones.get('solicitudes').get('solicitudes')

    try:
        for solicitud in solicitudes:
            id = solicitud.get('id_solicitud')

            solicitud_a = Solicitud.query.get(id)
            solicitud_a.estado = recolector

        db.session.commit()
        return jsonify({'mensaje':'Solicitudes asignadas exitosamente','icono':'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al asignar la solicitudes. Intente nuevamente','icono':'error'})
    finally:
        db.session.close()

  