from flask import render_template, Blueprint, request, jsonify
from app.models.models_barrios import Barrio
from app.models import db

barrios = Blueprint('barrio', __name__)

@barrios.route('/barrios', methods=['GET'])
def obtener_barrios():
    id_comuna = request.args.get('id_comuna')
    barrios = Barrio.query.filter_by(id_comuna=id_comuna).all()
    barrios_data = [{'id': barrio.id_barrio, 'nombre': barrio.nombre} for barrio in barrios]

    return jsonify(barrios_data)