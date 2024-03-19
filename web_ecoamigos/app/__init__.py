# app/__init__.py

from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import db
from flask_apscheduler import APScheduler
from flask import render_template
from functools import wraps
from flask import abort
from flask_login import current_user
from datetime import datetime
import pytz

def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
timezone = pytz.timezone('America/Bogota')
fecha_actual = datetime.now(timezone)

# Configuración de APScheduler
scheduler = APScheduler()
scheduler.init_app(app)

from app import routes

@app.errorhandler(405)
def acceso_no_autorizado(e):
    return render_template('error_acceso.html'), 405


