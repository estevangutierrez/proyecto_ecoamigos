from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Recolector
from flask_login import login_required
from app.models import db
from app import roles_required

recolector = Blueprint('recolector', __name__)

@recolector.route('/recolector')
@login_required
@roles_required('RECOLECTOR')
def recolector_home():
    return render_template('administrador.html')
