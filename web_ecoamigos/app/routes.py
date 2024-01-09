from app import app

from app.controllers.main import main
from app.controllers.auth import auth
from app.controllers.admin import admin
from app.controllers.recolector import recolector

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(recolector)