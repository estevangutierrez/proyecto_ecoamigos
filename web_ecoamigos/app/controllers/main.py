from flask import Blueprint, render_template
from app.models.models_registros import Visita
from app.models.models_roles import Proveedor
from app.models import db, func

main = Blueprint('main',__name__)

@main.route('/')
def index():
    total_proveedores = Proveedor.query.count()
    total_visitas = Visita.query.count()
    suma_cant_recolectada = db.session.query(func.sum(Visita.cant_recolectada)).scalar()

    return render_template('index.html', total_proveedores=total_proveedores,total_visitas=total_visitas,suma_cant_recolectada=suma_cant_recolectada)

@main.route('/blog')
def blog():
    return render_template('blog.html')