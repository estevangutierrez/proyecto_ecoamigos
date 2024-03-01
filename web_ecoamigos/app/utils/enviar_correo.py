import os
import base64
import json
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Define el alcance de acceso necesario para enviar correos electrónicos.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Ruta al archivo JSON de las credenciales que descargaste.
CREDENTIALS_FILE = 'C:/Users/Estevan/Desktop/proyecto_ecoamigos_1.2.0/web_ecoamigos/app/utils/client_secret_942503781738-bjc2ehu4amq499lq61c23d46jjqd8tsl.apps.googleusercontent.com.json'

# Nombre del archivo donde se almacenarán los tokens de acceso.
TOKEN_FILE = 'C:/Users/Estevan/Desktop/proyecto_ecoamigos_1.2.0/web_ecoamigos/app/utils/tokens.json'

# Definir la dirección de redirección fija.
REDIRECT_URI = "http://localhost:65412/"

def obtener_credenciales():
    creds = None

    # Intenta cargar las credenciales desde el archivo
    try:
        with open(TOKEN_FILE, 'r') as token:
            creds = google.oauth2.credentials.Credentials.from_authorized_user_info(
                json.load(token), SCOPES)
    except FileNotFoundError:
        pass
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            with open(TOKEN_FILE, 'r') as token:
                creds = google.oauth2.credentials.Credentials.from_authorized_user_info(
                    json.load(token), SCOPES)
            pass

    return creds



def enviar_correo(destinatario, cuerpo_correo, asunto="¡Bienvenido a EcoAmigos-Web!"):
    creds = obtener_credenciales()

    # Resto del código (sin cambios)
    # Crea una instancia de la API de Gmail.
    service = build('gmail', 'v1', credentials=creds)

    # Crea el mensaje de correo electrónico.
    message = MIMEText(cuerpo_correo)
    message['to'] = destinatario
    message['subject'] = asunto

    # Codifica el mensaje en base64.
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # Envía el correo electrónico.
    try:
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print('Correo electrónico enviado. ID del mensaje: %s' % message['id'])
    except Exception as e:
        print('Error al enviar el correo electrónico: %s' % str(e))
