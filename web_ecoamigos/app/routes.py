from app import app

from app.controllers.main import main
from app.controllers.auth import auth
from app.controllers.admin import admin
from app.controllers.recolector import recolector
from app.controllers.barrios import barrios
from app.controllers.proveedor import proveedor
from app.controllers.publicaciones import publicaciones

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(recolector)
app.register_blueprint(barrios)
app.register_blueprint(proveedor)
app.register_blueprint(publicaciones)