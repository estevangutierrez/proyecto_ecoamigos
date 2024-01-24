from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Proveedor
from app.models.models_registros import Solicitud
from flask_login import login_required, current_user
from app.models import db
from app import roles_required

proveedor = Blueprint('proveedor', __name__)

@proveedor.route('/proveedor')
@login_required
@roles_required('PROVEEDOR')
def proveedor_home():
    return render_template('administrador.html')


