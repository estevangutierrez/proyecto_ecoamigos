from flask import render_template, Blueprint, request, jsonify
from app.models.models_roles import Recolector
from flask_login import login_required
from app.models import db

recolector = Blueprint('recolector', __name__)

@recolector.route('/recolector_home')
@login_required
def recolector_home():
    return render_template('recolector.html')
