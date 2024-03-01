from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Proveedor
from app.models.models_registros import Solicitud, Visita
from flask_login import login_required, current_user
from app.models import db
from datetime import datetime
from app import roles_required
from app.utils.generar_token import generar_token


proveedor = Blueprint('proveedor', __name__)

locale = 'es_ES'

@proveedor.route('/proveedor')
@login_required
@roles_required('PROVEEDOR')
def proveedor_home():
    proveedor = Proveedor.query.get(current_user.id)
    id = current_user.id
    consulta = Visita.query.filter_by(id_proveedor=id).all()


    visitas = []
    for visita in consulta:
        datos = {
            'id': visita.id_visita,
            'fecha': visita.fecha_recoleccion,
            'cantidad': visita.cant_recolectada,
            'valor': visita.costo,
            'puntos': visita.puntos
        }
        visitas.append(datos)

    solicitud_p = db.session.query(Solicitud).filter(Solicitud.id_proveedor==proveedor.id_proveedor,Solicitud.estado!='finalizada').first()
    return render_template('dashboard_grid.html', proveedor=proveedor,solicitud_p=solicitud_p,visitas=visitas)

@proveedor.route('/proveedor/solicitudes')
@login_required
@roles_required('PROVEEDOR')
def cargar_solicitudes():
    id = current_user.id
    consulta = Visita.query.filter(id_proveedor=id).all()
    visitas = []
    for visita in consulta:
        datos = {
            'id': visita.id_visita,
            'fecha': visita.fecha_recoleccion,
            'cantidad': visita.cant_recolectada,
            'valor': visita.costo,
            'puntos': visita.puntos
        }
        visitas.append(datos)

    return render_template('proveedor.html', visitas=visitas)

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
    solicitud_pendiente = db.session.query(Solicitud).filter(Solicitud.id_proveedor==id,Solicitud.estado!='finalizada').first()
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
    fecha_solicitud = datetime.now()
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

