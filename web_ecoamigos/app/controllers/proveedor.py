from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Proveedor
from app.models.models_registros import Solicitud
from flask_login import login_required, current_user
from app.models import db
from datetime import datetime
from app import roles_required

proveedor = Blueprint('proveedor', __name__)

@proveedor.route('/proveedor')
@login_required
@roles_required('PROVEEDOR')
def proveedor_home():
    return render_template('administrador.html')

@proveedor.route('/proveedor/solicitudes')
@login_required
@roles_required('PROVEEDOR')
def cargar_solicitudes():
    return render_template('proveedor.html')

@proveedor.route('/proveedor/enviar_solicitud', methods=['POST'])
@login_required
@roles_required('PROVEEDOR')
def enviar_solicitud():
    datos = request.get_json()
    id = current_user.id
    proveedor = Proveedor.query.filter_by(id_proveedor=id).first()

    id_proveedor = proveedor.id_proveedor
    fecha_solicitud = datetime.now()
    cantidad_aprox = datos.get('cantidad')
    detalle = datos.get('detalle')

    solicitud = Solicitud(
        id_proveedor=id_proveedor, 
        fecha_solicitud=fecha_solicitud,
        cantidad_aprox=int(cantidad_aprox),
        detalle=detalle
    )

    db.session.add(solicitud)

    try:
        db.session.commit()
        return jsonify({'mensaje':'Solicitud creada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al crear la solicitud'}), 500
    finally:
        db.session.close()

