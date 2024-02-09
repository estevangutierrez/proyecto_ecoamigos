from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Recolector, Proveedor
from app.models.models_registros import Solicitud
from app.models.models_barrios import Barrio
from flask_login import login_required, current_user
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

    
    print(data_dict)
    return render_template("recolector.html",solicitudes=solicitudes)

# @recolector.route('/recolector/solicitudes')
# @login_required
# @roles_required('RECOLECTOR')
# def cargar_solicitudes():
#     informacion = db.session.query(Solicitud, Proveedor).join(Proveedor, Solicitud.id_proveedor == Proveedor.id_proveedor).all()
#     print(informacion)
#     solicitudes_na = Solicitud.query.filter_by(estado='pendiente')
#     solicitudes_asignadas = Solicitud.query.filter_by(estado=str(current_user.id))
#     solicitudes_cerradas = Solicitud.query.filter_by(estado='cerrada')

#     return render_template(
#                     'solicitudes-rec.html',
#                     solicitudes_na=solicitudes_na,
#                     solicitudes_asignadas=solicitudes_asignadas,
#                     solicitudes_cerradas=solicitudes_cerradas
#                 )

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
    