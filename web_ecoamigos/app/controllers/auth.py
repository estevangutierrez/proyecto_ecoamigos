from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from app.models.usuarios import Usuario
from app.models.models_roles import Proveedor, Administrador, Recolector
from app.models.models_barrios import Comuna, Barrio
from app.utils.enviar_correo import enviar_correo
from datetime import datetime
from app.models import db

auth = Blueprint('auth', __name__)

fecha = datetime.now().strftime('%d/%m/%Y %I:%M %p')


@auth.route('/pagina_login')
def pagina_login():
    comunas = Comuna.query.all()
    return render_template('login.html',comunas=comunas)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    id = data.get('usuario')
    contrasena = data.get('contrasena')

    user = Usuario.query.filter_by(id=id).first()

    if user and user.estado == True and user.verificar_contrasena(contrasena):

        login_user(user)
        session['user_id'] = user.id
        
        if user.rol == 'ADMINISTRADOR':
            return jsonify({'success': True, 'redirect_url': url_for('admin.admin_home')})
        elif user.rol == 'RECOLECTOR':
            return jsonify({'success': True, 'redirect_url': url_for('recolector.recolector_home')})
        elif user.rol == 'PROVEEDOR':
            return jsonify({'success': True, 'redirect_url': url_for('proveedor.proveedor_home')})
        
    return jsonify({'success': False})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

@auth.route('/cambiar_contrasena', methods=['PUT'])
@login_required
def cambiar_contrasena():

    datos = request.get_json()

    id = datos.get('id_usuario')
    contrasena_actual = datos.get('contrasena_actual')
    contrasena_nueva = datos.get('contrasena_nueva')

    usuario = Usuario.query.get(id)

    if usuario:
        try:
            cambio_is_ok = usuario.cambiar_contrasena(contrasena_actual,contrasena_nueva)

            if not cambio_is_ok:
                return jsonify({'mensaje':'La contraseña actual no es correcta','icono':'warning'})
            
            mensaje_cambio_contrasena = f'''
Estimado/a {usuario.nombre.split()[0].capitalize()},

Te informamos que tu contraseña de Ecoamigos ha sido actualizada con éxito el {fecha}. Si no realizaste esta acción, te recomendamos que te pongas en contacto con nosotros de inmediato para investigar cualquier actividad no autorizada.

¡Gracias por confiar en nosotros!

Atentamente,
El equipo de Ecoamigos
'''
            enviar_correo(usuario.correo,mensaje_cambio_contrasena,asunto='Cambiaste tu contraseña')
            db.session.commit()
            
            return jsonify({'mensaje':'La contraseña fue cambiada exitosamente','icono':'success'})
            
        except Exception as e:
            db.session.rollback()
            print('El error fue', e)
            return jsonify({'mensaje':'Hubo un error al actualizar la contraseña','icono':'error'})
        finally:
            db.session.close()

    return jsonify({'mensaje':'Usuario no encontrado','icono':'error'})

@auth.route('/mi_perfil', methods=['GET'])
def cargar_perfil():
    id = current_user.id 
    rol = current_user.rol

    comunas = Comuna.query.all()
    barrios = Barrio.query.all()

    if rol == 'ADMINISTRADOR':
        usuario = Administrador.query.get(id)
    elif rol == 'PROVEEDOR':
        usuario = Proveedor.query.get(id)
    elif rol == 'RECOLECTOR':
        usuario = Recolector.query.get(id)

    return render_template('perfil.html',usuario=usuario, comunas=comunas, barrios=barrios)

            
        




