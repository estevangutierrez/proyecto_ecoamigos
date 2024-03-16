import random
import string

def generar_contrasena():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(8))

    return contrasena