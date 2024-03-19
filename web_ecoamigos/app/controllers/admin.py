from flask import render_template, Blueprint, request, jsonify
from app.models.usuarios import Usuario
from app.models.models_roles import Administrador, Recolector, Proveedor
from app.models.models_barrios import Comuna, Barrio
from app.models.models_publico import Noticia
from app.models.models_registros import Solicitud, Visita, Canjeo
from app.utils.generar_contrasena import generar_contrasena
from app.utils.enviar_correo import enviar_correo
from flask_login import login_required, current_user
from app import roles_required
import base64
from app.models import db

admin = Blueprint('admin', __name__)


def crear_usuario(id, nombre, correo, rol, contrasena):
    nuevo_usuario = Usuario(id=id,nombre=nombre,correo=correo,rol=rol)
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

@admin.route('/administrador/actualizar_datos', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def actualizar_datos():
    datos = request.get_json()

    id = datos.get('cedula')

    nuevos_datos = {
        'nombre': datos.get('nombre').upper(),
        'correo': datos.get('correo').upper(),
        'celular': datos.get('celular')
    }

    administrador = Administrador.query.get(id)
    if administrador:
       usuario = Usuario.query.get(id)
       try:
           usuario.actualizar_usuario(nombre=datos.get('nombre'), correo=datos.get('correo'))
           administrador.actualizar_datos(nuevos_datos)
           db.session.commit()
           mensaje_actualización_datos = '''
Hola,

Queremos informarte que se han realizado actualizaciones en tus datos de usuario. Si realizaste estos cambios, ignora este mensaje. En caso contrario, por favor, contáctanos lo antes posible para investigar cualquier actividad sospechosa.

¡Gracias por ser parte de nuestra comunidad!

Saludos cordiales,
El equipo de Ecofriendly
'''
           enviar_correo(datos.get('correo'),mensaje_actualización_datos,asunto='Actualizaste tus datos')

           return jsonify({'mensaje':'Datos actualizados correctamente','icono':'success'})
       
       except Exception as e:
           print(e)
           db.session.rollback()
           return jsonify({'mensaje':'Error al actualizar los datos','icono':'error'})
       finally:
           db.session.close()
    
    return jsonify({'mensaje':f'No se encontró administrador con el ID {id}','icono':'error'})

@admin.route('/administrador/solicitudes')
@login_required
@roles_required('ADMINISTRADOR')
def solicitudes():
    datos = (
        db.session.query(Solicitud, Proveedor)
        .join(Proveedor, Solicitud.id_proveedor == Proveedor.id_proveedor)
        )
    
    proveedores = Proveedor.query.all()
    
    solicitudes_asignadas = (
        db.session.query(Solicitud, Recolector)
        .join(Recolector, Solicitud.estado == Recolector.id_recolector)
        )
    
    solicitudes_vencidas = Solicitud.query.filter_by(estado='vencida').all()

    historial_visitas = (
        db.session.query(Visita, Recolector, Proveedor)
        .join(Recolector, Visita.id_recolector == Recolector.id_recolector)
        .join(Proveedor, Visita.id_proveedor == Proveedor.id_proveedor)
        .all()
        )
    
    recolectores_data = Recolector.query.all()

    solicitudes = []
    recolectores = []
    solicitudes_a = []
    solicitudes_v = []
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
            'asignado': recolector.nombre,
            'token': solicitud_a.token
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
    
    for solicitud_v in solicitudes_vencidas:
        vencidas_dict = {
            'id':solicitud_v.id_solicitud,
            'proveedor':solicitud_v.id_proveedor,
            'fecha_solicitud':solicitud_v.fecha_solicitud,
            'cantidad':solicitud_v.cantidad_aprox
        }

        solicitudes_v.append(vencidas_dict)


    return render_template("solicitudes.html", solicitudes=solicitudes, recolectores=recolectores,solicitudes_a=solicitudes_a, visitas=visitas, solicitudes_v=solicitudes_v, proveedores=proveedores)


@admin.route('/administrador/canjeos')
@login_required
@roles_required('ADMINISTRADOR')
def cargar_canjeos():
    consulta = db.session.query(Canjeo, Proveedor).join(Proveedor, Canjeo.id_proveedor==Proveedor.id_proveedor).all()
    canjeos = []

    for canjeo,proveedor in consulta:
        canjeo_dict = {
            'id':canjeo.id_canjeo,
            'nombre':proveedor.nombre,
            'cedula':canjeo.id_proveedor,
            'banco':canjeo.medio,
            'cuenta':canjeo.cuenta,
            'puntos':canjeo.puntos,
            'valor':canjeo.valor,
            'estado':canjeo.estado
        }
        canjeos.append(canjeo_dict)

        canjeos.reverse()

    return render_template('gestCanjeos.html',canjeos=canjeos)

@admin.route('/administrador/canjeos/confirmar_canjeo', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def confirmar_canjeo():
    datos = request.get_json()
    id_canjeo = datos.get('id_canjeo')
    imagen_base64 = datos.get('imagenURL').split(',')[1]
    imagen_binario = base64.b64decode(imagen_base64)
    administrador = current_user.id

    canjeo = Canjeo.query.get(id_canjeo)
    proveedor = Proveedor.query.get(canjeo.id_proveedor)

    correo = proveedor.correo

    if canjeo is None:
        return jsonify({'mensaje':'Canjeo no existente, actualiza la página','icono':'error'})
    
    try:
        canjeo.soporte = imagen_binario
        canjeo.id_administrador = administrador
        canjeo.estado = 'canjeado'

        mensaje_confirmacion = f'''
¡Hola!

Queremos informarte que ya realizamos el pago de tu canjeo por un valor de ${canjeo.valor}. Por favor, revisa tu cuenta para confirmar los detalles del canjeo realizado.

Recuerda que cada vez que reciclas aceite de cocina usado, estás ayudando a cuidar nuestro planeta y ganando puntos para ti.

Gracias por ser parte de nuestro movimiento hacia un mundo más limpio y sostenible.

¡Sigue acumulando puntos y haciendo la diferencia!

Atentamente,
El equipo de Ecofriendly
'''
        enviar_correo(correo,mensaje_confirmacion,asunto='Hemos realizado tu canjeo')


        db.session.commit()
        return jsonify({'mensaje':'Canjeo realizado exitosamente','icono':'success'})
    except Exception as e:
        db.session.rollback()
        print(f'El error fue {e}')
        return jsonify({'mensaje':'Hubo un error al realizar el canjeo','icono':'error'})
    finally:
        db.session.close()

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
    contrasena = generar_contrasena()
    rol = 'ADMINISTRADOR'

    user = Usuario.query.filter_by(id=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,correo,rol,contrasena)
    nuevo_admin = Administrador(id_admin=int(id),nombre=nombre,correo=correo,celular=telefono)


    db.session.add(nuevo_usuario)
    db.session.add(nuevo_admin)
    db.session.commit()
    db.session.close()

    mensaje_bienvenida = f'''
Hola { nombre.split()[0].capitalize() },

¡Te damos una calurosa bienvenida a la familia Ecofriendly!

Estamos emocionados de tenerte con nosotros. A continuación, encontrarás tus credenciales de acceso en tu rol de { rol.lower() } para comenzar tu experiencia:

Usuario: {id}
Contraseña: {contrasena}

Por favor, inicia sesión con estos datos y recuerda cambiar tu contraseña después del primer inicio de sesión.

¡Esperamos que disfrutes de tu tiempo con nosotros y contribuyas a hacer del mundo un lugar más sostenible!

¡Bienvenido/a de nuevo!

Con cariño,
El equipo de Ecofriendly
'''

    enviar_correo(correo,mensaje_bienvenida)

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
    contrasena = generar_contrasena()
    rol = 'RECOLECTOR'

    user = Usuario.query.filter_by(id=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,correo,rol,contrasena)
    nuevo_recolector = Recolector(id_recolector=int(id),nombre=nombre,direccion=direccion,id_comuna=comuna,id_barrio=barrio,correo=correo,celular=telefono)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_recolector)

    try:
        mensaje_bienvenida = f'''
Hola { nombre.split()[0].capitalize() },

¡Te damos una calurosa bienvenida a la familia Ecofriendly!

Estamos emocionados de tenerte con nosotros. A continuación, encontrarás tus credenciales de acceso en tu rol de { rol.lower() } para comenzar tu experiencia:

Usuario: {id}
Contraseña: {contrasena}

Por favor, inicia sesión con estos datos y recuerda cambiar tu contraseña después del primer inicio de sesión.

¡Esperamos que disfrutes de tu tiempo con nosotros y contribuyas a hacer del mundo un lugar más sostenible!

¡Bienvenido/a de nuevo!

Con cariño,
El equipo de Ecofriendly
'''

        enviar_correo(correo,mensaje_bienvenida)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print('EL ERROR FUE ', e)
        return jsonify({'success':False})
    finally:
        db.session.close()


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
    comunas = Comuna.query.all()
    return render_template('proveedores.html',proveedores=proveedores, comunas=comunas)


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
    contrasena = generar_contrasena()
    puntos = 0
    rol = 'PROVEEDOR'

    user = Proveedor.query.filter_by(id_proveedor=id).first()

    if user:
        return jsonify({'success': False})

    nuevo_usuario = crear_usuario(id,nombre,correo,rol,contrasena)
    nuevo_proveedor = Proveedor(id_proveedor=int(id),tipo_prov=int(tipo),nombre=nombre,direccion=direccion,id_comuna=comuna,id_barrio=barrio,correo=correo,celular=telefono,puntos=puntos)

    db.session.add(nuevo_usuario)
    db.session.add(nuevo_proveedor)

    try:
        mensaje_bienvenida = f'''
Hola { nombre.split()[0].capitalize() },

¡Te damos una calurosa bienvenida a la familia Ecofriendly!

Estamos emocionados de tenerte con nosotros. A continuación, encontrarás tus credenciales de acceso en tu rol de { rol.lower() } para comenzar tu experiencia:

Usuario: {id}
Contraseña: {contrasena}

Por favor, inicia sesión con estos datos y recuerda cambiar tu contraseña después del primer inicio de sesión.

¡Esperamos que disfrutes de tu tiempo con nosotros y contribuyas a hacer del mundo un lugar más sostenible!

¡Bienvenido/a de nuevo!

Con cariño,
El equipo de Ecofriendly
'''
        db.session.commit()
        enviar_correo(correo,mensaje_bienvenida)
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print('EL ERROR FUE ', e)
        return jsonify({'success':False})
    finally:
        db.session.close()


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

@admin.route('/administrador/solicitudes/rechazar', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def rechazar_solicitud():
    id_solicitud = request.get_json().get('id_solicitud')

    try:
        solicitud = Solicitud.query.get(id_solicitud)
        proveedor = Proveedor.query.get(solicitud.id_proveedor)
        nombre = proveedor.nombre
        correo = proveedor.correo

        solicitud.estado = 'rechazada'
        solicitud.liberar_token()

        cuerpo_correo = f'''Hola, { nombre }!
        Hemos rechazado tu solicitud {id_solicitud} porque nos lo has pedido.
        Si esto no es correcto, por favor, comunicate con nosotros.
        Atte: Equipo de Ecofriendly MVD'''
        
        enviar_correo(correo,cuerpo_correo,asunto='Tu solicitud ha sido rechazada')

        db.session.commit()
        return jsonify({'mensaje':'Solicitud rechazada exitosamente','icono':'success'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al rechazar la solicitud','icono':'error'})
    
    finally:
        db.session.close()

  