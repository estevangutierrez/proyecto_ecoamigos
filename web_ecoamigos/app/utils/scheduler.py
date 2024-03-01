# app/utils/scheduler.py

from app import db
from datetime import datetime, timedelta
from app.models.models_registros import Solicitud

def actualizar_solicitudes_vencidas(app):
    with app.app_context():
        solicitudes_vencidas = Solicitud.query.filter(Solicitud.estado == 'pendiente').filter(Solicitud.fecha_solicitud < (datetime.now() - timedelta(days=3)),).all()

        for solicitud in solicitudes_vencidas:
            solicitud.estado = 'vencida'

        print('Solicitudes vencidas actualizadas')
    
        db.session.commit()
        db.session.close()
