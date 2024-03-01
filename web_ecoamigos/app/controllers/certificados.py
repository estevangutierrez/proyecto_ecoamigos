from flask import render_template, make_response, jsonify, Blueprint
from app.models import db
from app.models.models_registros import Certificado, Visita
from app.models.models_roles import Administrador, Recolector, Proveedor
import pdfkit

certificados = Blueprint('certificados', __name__)

wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' # Reemplaza con la ruta correcta
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

@certificados.route('/generar_pdf/<int:id_visita>')
def generar_pdf(id_visita):

    certificado = (
        db.session.query(
            Certificado.id_certificado,
            Visita.id_visita,
            Proveedor.id_proveedor.label('id_proveedor'),
            Proveedor.nombre.label('nombre_proveedor'),
            Recolector.id_recolector.label('id_recolector'),
            Recolector.nombre.label('nombre_recolector'),
            Visita.fecha_recoleccion,
            Visita.cant_recolectada,
            Certificado.tipo
        )
        .join(Visita, Certificado.id_visita == Visita.id_visita)
        .join(Proveedor, Visita.id_proveedor == Proveedor.id_proveedor)
        .join(Recolector, Visita.id_recolector == Recolector.id_recolector)
        .filter(Visita.id_visita == id_visita)
        .first()
    )

    # Comprobar si se encontró un certificado
    if certificado is None:
        return render_template('error.html', mensaje='No se encontró certificado para la visita proporcionada')

    # Renderiza la plantilla HTML con los datos del certificado
    html = render_template('plantilla_certificado.html', certificado=certificado)

    print(certificado)

    # Convierte el HTML a PDF
    pdf = pdfkit.from_string(html, False, configuration=config)

    # Crea una respuesta Flask con el PDF generado
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=certificado_recoleccion_{certificado.id_certificado}.pdf'

    return response