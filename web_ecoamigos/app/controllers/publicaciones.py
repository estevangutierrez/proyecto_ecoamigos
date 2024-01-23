from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
import base64
from app.models.models_publico import Noticia
from flask_login import login_required, current_user
from app.models import db

publicaciones = Blueprint('publicaciones', __name__)

@publicaciones.route('/crear_publicacion', methods=['POST'])
@login_required
def crear_publicacion():
    datos = request.get_json()

    id_admin = current_user.id
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')
    fecha = datetime.now()
    imagen_base64 = datos.get('imagen')
    imagen_binario = base64.b64decode(imagen_base64.split(',')[1])

    datos_dict = {
        'id_admin' : id_admin,
        'titulo' : titulo,
        'descripcion' : descripcion,
        'fecha' : fecha,
        'recurso' : imagen_binario
    }

    try:
        Noticia.agregar_noticia(datos_dict)
        return jsonify({'mensaje':'Publicación creada con éxito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al crear la publicación'}), 500
    finally:
        db.session.close()



