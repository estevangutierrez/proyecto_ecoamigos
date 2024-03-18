from flask import Blueprint, request, jsonify
import base64
from app.models.models_publico import Noticia
from flask_login import login_required, current_user
from app.models import db
from base64 import b64encode
from app import roles_required, fecha_actual


publicaciones = Blueprint('publicaciones', __name__)

@publicaciones.route('/crear_publicacion', methods=['POST'])
@login_required
@roles_required('ADMINISTRADOR')
def crear_publicacion():
    datos = request.get_json()

    try:
        id_admin = current_user.id
        titulo = datos.get('titulo')
        descripcion = datos.get('descripcion')
        fecha = fecha_actual
        imagen_base64 = datos.get('imagen_data').split(',')[1]
        imagen_binario = base64.b64decode(imagen_base64)
        nueva_publicacion = Noticia(id_admin=id_admin,titulo=titulo,descripcion=descripcion,fecha=fecha,recurso=imagen_binario)
        db.session.add(nueva_publicacion)
        db.session.commit()
        return jsonify({'mensaje':'Publicación creada con éxito'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al crear la publicación'}), 500
    finally:
        db.session.close()


@publicaciones.route('/publicaciones/editar/<int:id>', methods=['PUT'])
@login_required
@roles_required('ADMINISTRADOR')
def editar_publicacion(id):
    datos = request.get_json()

    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')   
    imagen_data = datos.get('imagen')

    print(f'datos imagen: {imagen_data}')

    noticia = Noticia.query.get(id)

    try:
        if imagen_data:
            imagen_base64 = imagen_data.split(',')[1]
            imagen_binario = base64.b64decode(imagen_base64)
            noticia.editar_publicacion(titulo=titulo,descripcion=descripcion,imagen=imagen_binario)
        else:
            noticia.editar_publicacion(titulo=titulo,descripcion=descripcion)

        db.session.commit()

        return jsonify({'mensaje':'Publicacion editada exitosamente','icono':'success'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje':'Error al editar la publicacion','icono':'error'})
    
    finally:
        db.session.close()

@publicaciones.route('/publicaciones/eliminar/<int:id>', methods=['DELETE'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminar_publicacion(id):
    noticia = Noticia.query.get(id)

    if noticia:
        db.session.delete(noticia)
        db.session.commit()
        db.session.close()
        return jsonify({'mensaje':'Publicacion eliminada exitosamente','icono':'success'})
    else:
        return jsonify({'mensaje':'Error al eliminar la noticia','icono':'error'})
    

@publicaciones.route('/blog/publicaciones')
def obtener_publicaciones():
    noticias = Noticia.query.all()

    noticias_data = []

    for noticia in noticias:
        imagen_blob = noticia.recurso
        imagen_base64 = b64encode(imagen_blob).decode('utf-8')

        noticias_data.append({
            'titulo': noticia.titulo,
            'descripcion': noticia.descripcion,
            'fecha': noticia.fecha,
            'imagen': imagen_base64
        })
    
    noticias_data.reverse()

    return jsonify(noticias_data)