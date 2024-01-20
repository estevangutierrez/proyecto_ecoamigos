from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Proveedor
from flask_login import login_required
from app.models import db

proveedor = Blueprint('proveedor', __name__)

@proveedor.route('/proveedor_home')
@login_required
def proveedor_home():
    return render_template('proveedor.html')