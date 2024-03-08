from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Recolector, Proveedor
from app.models.models_registros import Solicitud, Visita, Certificado
from app.models.models_barrios import Barrio
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db
from app import roles_required

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

# @recolector.route('/recolector/solicitudes')
# @login_required
# @roles_required('RECOLECTOR')
# def cargar_solicitudes():
#     informacion = db.session.query(Solicitud, Proveedor).join(Proveedor, Solicitud.id_proveedor == Proveedor.id_proveedor).all()
#     solicitudes_na = Solicitud.query.filter_by(estado='pendiente')
#     solicitudes_asignadas = Solicitud.query.filter_by(estado=str(current_user.id))
#     solicitudes_cerradas = Solicitud.query.filter_by(estado='cerrada')

#     return render_template(
#                     'solicitudes-rec.html',
#                     solicitudes_na=solicitudes_na,
#                     solicitudes_asignadas=solicitudes_asignadas,
#                     solicitudes_cerradas=solicitudes_cerradas
#                 )

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
    fecha_recoleccion=datetime.now(),
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
    