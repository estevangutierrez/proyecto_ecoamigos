from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Recolector, Proveedor
from app.models.models_registros import Solicitud, Visita, Certificado
from app.models.models_barrios import Barrio
from app.models.usuarios import Usuario
from flask_login import login_required, current_user
from app.models import db
from app.utils.enviar_correo import enviar_correo
from app import roles_required, fecha_actual

recolector = Blueprint('recolector', __name__)

@recolector.route('/recolector')
@login_required
@roles_required('RECOLECTOR')
def recolector_home():
    informacion = (
        db.session.query(Solicitud, Proveedor, Barrio)
        .join(Proveedor, Solicitud.id_proveedor == Proveedor.id_proveedor)
        .join(Barrio, Proveedor.id_barrio == Barrio.id_barrio).all()
    )
    
    solicitudes = []
    for solicitud, proveedor, barrio in informacion:
        data_dict = {
        "id_solicitud": solicitud.id_solicitud,
        "fecha": solicitud.fecha_solicitud,
        "proveedor": proveedor.nombre,
        "direccion": proveedor.direccion,
        "comuna": proveedor.id_comuna,
        "barrio": barrio.nombre,
        "cantidad": solicitud.cantidad_aprox,
        "detalle": solicitud.detalle,
        "estado": solicitud.estado
        }
        solicitudes.append(data_dict)        

    
    return render_template("recolector.html",solicitudes=solicitudes)

@recolector.route('/recolector/historial')
def cargar_historial():
    id = current_user.id

    consulta = db.session.query(Visita, Proveedor).join(Proveedor, Visita.id_proveedor==Proveedor.id_proveedor).filter(Visita.id_recolector==id)

    visitas = []

    for visita, proveedor in consulta:
        dict = {
            'id': visita.id_visita,
            'proveedor': proveedor.nombre,
            'fecha': visita.fecha_recoleccion,
            'cantidad': visita.cant_recolectada,
            'valor': visita.costo
        }

        visitas.append(dict)

    return render_template('historial.html',visitas=visitas)


@recolector.route('/recolector/actualizar_datos', methods=['PUT'])
@login_required
@roles_required(['RECOLECTOR','ADMINISTRADOR'])
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

    recolector = Recolector.query.get(id)
    if recolector:
       usuario = Usuario.query.get(id)
       try:
           usuario.actualizar_usuario(nombre=nuevos_datos.get('nombre'), correo=nuevos_datos.get('correo'))
           recolector.actualizar_datos(nuevos_datos)
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
           db.session.rollback()
           print(e)
           return jsonify({'mensaje':'Error al actualizar los datos','icono':'error'})
       finally:
           db.session.close()
    
    return jsonify({'mensaje':f'No se encontró recolector con el ID {id}','icono':'error'})

@recolector.route('/recolector/solicitudes/confirmar', methods=['POST'])
@login_required
@roles_required('RECOLECTOR')
def confirmar_solicitud():
    datos = request.get_json()

    id_solicitud = datos.get('id_solicitud')
    cantidad_recolectada = datos.get('cantidad')
    token = datos.get('token')

    solicitud = Solicitud.query.get(id_solicitud)

    id_recolector=int(solicitud.estado),
    id_proveedor=int(solicitud.id_proveedor),
    fecha_recoleccion=fecha_actual,
    costo=(int(cantidad_recolectada)*2500),
    puntos = (int(cantidad_recolectada)/2)

    if not solicitud:
        return jsonify({'mensaje':'Esta solicitud ya fue visitada','icono':'error'})
    
    try:
        if solicitud.token != int(token):
            return({'token_incorrecto':True})
    
        visita = Visita(
            id_solicitud=id_solicitud,
            id_recolector=id_recolector,
            id_proveedor=id_proveedor,
            fecha_recoleccion=fecha_recoleccion,
            cant_recolectada=cantidad_recolectada,
            costo=costo,
            puntos=puntos
        )

        solicitud.estado = 'finalizada'
        solicitud.liberar_token()

        proveedor = Proveedor.query.get(id_proveedor)
        proveedor.aumentar_puntos(puntos)
    
        db.session.add(visita)

        visita_c = Visita.query.filter_by(id_solicitud=id_solicitud).first()

        certificado = Certificado(
            id_visita=visita_c.id_visita, 
            tipo='recoleccion',
            )
        
        db.session.add(certificado)

        db.session.commit()

        return jsonify({'mensaje':'Visita finalizada exitosamente','icono':'success'})

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'mensaje':'Error al confirmar la visita','icono':'error'})
    
    finally:
        db.session.close()


@recolector.route('/recolector/aceptar_solicitud', methods=['PUT'])
@login_required
@roles_required('RECOLECTOR')
def aceptar_solicitud():
    datos = request.get_json()
    id_solicitud = datos.get('id_solicitud')
    solicitud = Solicitud.query.get(id_solicitud)

    if solicitud is None:
        return jsonify({'error':'Solicitud no encontrada'}), 404
    elif solicitud.estado != 'pendiente':
        return jsonify({'error':'Esta solicitud ya está asignada a un recolector'})
    
    id_recolector = current_user.id
    solicitud.aceptar_solicitud(id_recolector)

    try:
        db.session.commit()
        return jsonify({'ok': f'Solicitud asignada a {current_user.nombre}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al aceptar la solicitud'}), e
    finally:
        db.session.close()
