from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Proveedor
from app.models.models_registros import Solicitud, Visita, Canjeo
from flask_login import login_required, current_user
from app.models import db
from app.models.usuarios import Usuario
from app.utils.enviar_correo import enviar_correo
from app import roles_required, fecha_actual
from app.utils.generar_token import generar_token
import base64

proveedor = Blueprint('proveedor', __name__)

locale = 'es_ES'

@proveedor.route('/proveedor')
@login_required
@roles_required('PROVEEDOR')
def proveedor_home():
    proveedor = Proveedor.query.get(current_user.id)
    id = current_user.id
    consulta = Solicitud.query.filter_by(id_proveedor=id).all()

    solicitudes = []
    for solicitud in consulta:
        datos = {
            'id': solicitud.id_solicitud,
            'fecha': solicitud.fecha_solicitud,
            'cantidad': solicitud.cantidad_aprox,
            'estado': solicitud.estado,
        }
        solicitudes.append(datos)
    
    solicitudes.reverse()

    solicitud_p = db.session.query(Solicitud).filter(Solicitud.id_proveedor==proveedor.id_proveedor,Solicitud.estado!='finalizada').filter(Solicitud.estado!='rechazada').filter(Solicitud.estado!='vencida').first()
    return render_template('dashboard_grid.html', proveedor=proveedor,solicitud_p=solicitud_p,solicitudes=solicitudes)

@proveedor.route('/proveedor/actualizar_datos', methods=['PUT'])
@login_required
@roles_required(['PROVEEDOR','ADMINISTRADOR'])
def actualizar_datos():
    datos = request.get_json()

    id = datos.get('cedula')

    nuevos_datos = {
        'nombre': datos.get('nombre').upper(),
        'direccion': datos.get('direccion').upper(),
        'comuna': datos.get('comuna'),
        'barrio': datos.get('barrio'),
        'correo': datos.get('correo').upper(),
        'celular': datos.get('celular')
    }

    print(nuevos_datos)

    proveedor = Proveedor.query.get(id)
    if proveedor:
       usuario = Usuario.query.get(id)
       try:
           usuario.actualizar_usuario(nombre=datos.get('nombre'), correo=datos.get('correo'))
           proveedor.actualizar_datos(nuevos_datos)

           mensaje_actualización_datos = '''
Hola,

Queremos informarte que se han realizado actualizaciones en tus datos de usuario. Si realizaste estos cambios, ignora este mensaje. En caso contrario, por favor, contáctanos lo antes posible para investigar cualquier actividad sospechosa.

¡Gracias por ser parte de nuestra comunidad!

Saludos cordiales,
El equipo de Ecofriendly
'''
           enviar_correo(datos.get('correo'),mensaje_actualización_datos,asunto='Actualizaste tus datos')
           db.session.commit()

           return jsonify({'mensaje':'Datos actualizados correctamente','icono':'success'})
       
       except Exception as e:
           print(e)
           db.session.rollback()
           return jsonify({'mensaje':'Error al actualizar los datos','icono':'error'})
       finally:
           db.session.close()
    
    return jsonify({'mensaje':f'No se encontró proveedor con el ID {id}','icono':'error'})

@proveedor.route('/proveedor/recolecciones')
@login_required
@roles_required('PROVEEDOR')
def cargar_recolecciones():
    id = current_user.id
    consulta = db.session.query(Visita, Solicitud).join(Solicitud, Visita.id_solicitud==Solicitud.id_solicitud).filter_by(id_proveedor=id).all()

    recolecciones = []

    for visita, solicitud in consulta:
        recoleccion = {
            'id'        :visita.id_visita,
            'fecha'     :visita.fecha_recoleccion,
            'cantidad_s':solicitud.cantidad_aprox,
            'cantidad_r':visita.cant_recolectada,
            'puntos'    :visita.puntos,
            'valor'     :visita.costo
        }
        recolecciones.append(recoleccion)

    return render_template('recolecciones_prov.html',recolecciones=recolecciones)

@proveedor.route('/proveedor/enviar_solicitud', methods=['POST'])
@login_required
@roles_required(['PROVEEDOR','ADMINISTRADOR'])
def enviar_solicitud():
    datos = request.get_json()
    if current_user.rol == 'PROVEEDOR':
        id = current_user.id
    else:
        id = datos.get('proveedor')

    proveedor = Proveedor.query.filter_by(id_proveedor=id).first()
    solicitud_pendiente = (db.session.query(Solicitud)
                           .filter(Solicitud.id_proveedor==id,Solicitud.estado!='finalizada')
                           .filter(Solicitud.estado!='rechazada')
                           .filter(Solicitud.estado!='vencida').first()
                           )
    
    solicitudes = Solicitud.query.all()

    tokens = []

    for solicitud in solicitudes:
        token = solicitud.token
        tokens.append(token)     

    while True:
        nuevo_token = generar_token()

        if nuevo_token not in tokens:
            break

    if solicitud_pendiente:
        return jsonify({'existe':'Solicitud existente'})

    id_proveedor = proveedor.id_proveedor
    fecha_solicitud = fecha_actual
    cantidad_aprox = datos.get('cantidad')
    detalle = datos.get('detalle')
    token = nuevo_token

    solicitud = Solicitud(
        id_proveedor=id_proveedor, 
        fecha_solicitud=fecha_solicitud,
        cantidad_aprox=int(cantidad_aprox),
        detalle=detalle,
        token=token
    )

    db.session.add(solicitud)

    try:
        db.session.commit()
        return jsonify({'ok':'Solicitud creada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'Error al crear la solicitud'}), 500
    finally:
        db.session.close()

@proveedor.route('/proveedor/mis_canjeos')
@login_required
@roles_required('PROVEEDOR')
def cargar_canjeos():
    id_proveedor = current_user.id
    consulta = Canjeo.query.filter_by(id_proveedor=id_proveedor).all()
    canjeos = []

    for canjeo in consulta:
        canjeo_dict = {
            'id':canjeo.id_canjeo,
            'banco':canjeo.medio,
            'cuenta':canjeo.cuenta,
            'puntos':canjeo.puntos,
            'valor':canjeo.valor,
            'estado':canjeo.estado
        }
        canjeos.append(canjeo_dict)

    canjeos.reverse()

    return render_template('mis_canjeos.html',canjeos=canjeos)

@proveedor.route('/proveedor/mis_canjeos/soporte/<int:id>', methods=['GET'])
@roles_required('PROVEEDOR')
def cargar_comprobante(id):
    canjeo = Canjeo.query.get(id)

    soporte = canjeo.soporte
    imagen = base64.b64encode(soporte).decode('utf-8')

    return jsonify({'imagen':imagen})


@proveedor.route('/proveedor/canjear_puntos', methods=['POST'])
@login_required
@roles_required(['PROVEEDOR','ADMINISTRADOR'])
def canjear_puntos():
    datos = request.get_json()

    id_proveedor = current_user.id 
    medio = datos.get('banco')
    cuenta = datos.get('cuenta')
    puntos = int(datos.get('puntos'))
    valor = puntos*200
    fecha = fecha_actual

    canjeo_activo = db.session.query(Canjeo).filter(Canjeo.id_proveedor==id_proveedor,Canjeo.estado=='pendiente').first()

    if canjeo_activo:
        return jsonify({'mensaje':'Ya tienes una solicitud activa','icono':'error'})
    
    try:
        canjeo = Canjeo(id_proveedor=id_proveedor,medio=medio,cuenta=cuenta,puntos=puntos,valor=valor,fecha=fecha)
        proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
        proveedor.restar_puntos(puntos)

        db.session.add(canjeo)
        db.session.commit()
        return jsonify({'mensaje':'La solicitud de canjeo ha sido exitosa, recuerda que se atenderá el jueves más cercado a hoy.','icono':'success'})
    
    except Exception as e:
        db.session.rollback()
        print(f'el error fue {e}')
        return jsonify({'mensaje':'Error al solicitar el canjeo','icono':'error'})
    
    finally:
        db.session.close()

