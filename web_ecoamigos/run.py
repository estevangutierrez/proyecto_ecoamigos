# run.py
from app import app, scheduler
from app.utils.scheduler import actualizar_solicitudes_vencidas
import os

# Tarea programada para actualizar solicitudes vencidas cada 1 hora
scheduler.add_job(id='actualizar_solicitudes',func=actualizar_solicitudes_vencidas, args=[app], trigger='interval', hours=12)

if __name__ == '__main__':
    scheduler.start()  # Inicia el planificador de tareas
    app.run(debug=True)
    

