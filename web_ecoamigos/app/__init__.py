from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import db
from flask import render_template

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY']='eaaaR/5mM222%#2298Tf'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from app import routes

@app.errorhandler(405)
def acceso_no_autorizado(e):
    return render_template('error_acceso.html'), 405

