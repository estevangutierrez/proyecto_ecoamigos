from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from app.models.usuarios import Usuario
from app.models.models_barrios import Comuna

auth = Blueprint('auth', __name__)

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

    if user and user.verificar_contrasena(contrasena):

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



